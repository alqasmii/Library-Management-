# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class LibraryBorrow(models.Model):
    """Library borrow/loan with overdue tracking and state management."""
    _name = 'library.borrow'
    _description = 'Library Borrow'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'borrow_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    
    # Core relationships
    member_id = fields.Many2one(
        'library.member',
        string='Member',
        required=True,
        tracking=True,
        ondelete='restrict'
    )
    book_id = fields.Many2one(
        'library.book',
        string='Book',
        required=True,
        tracking=True,
        ondelete='restrict'
    )
    staff_id = fields.Many2one(
        'library.staff',
        string='Handled By',
        tracking=True,
        ondelete='set null'
    )
    
    # Dates
    borrow_date = fields.Date(
        string='Borrow Date',
        default=fields.Date.today,
        required=True,
        tracking=True
    )
    due_date = fields.Date(
        string='Due Date',
        required=True,
        tracking=True,
        help='Date by which the book should be returned'
    )
    return_date = fields.Date(
        string='Actual Return Date',
        tracking=True,
        help='Actual date when the book was returned'
    )
    
    # State management
    state = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True, tracking=True)
    
    # Computed fields
    borrow_duration = fields.Integer(
        string='Duration (days)',
        compute='_compute_borrow_duration',
        store=True
    )
    is_overdue = fields.Boolean(
        string='Is Overdue',
        compute='_compute_overdue_info',
        store=True
    )
    overdue_days = fields.Integer(
        string='Overdue Days',
        compute='_compute_overdue_info',
        store=True,
        help='Number of days overdue'
    )
    fine_amount = fields.Float(
        string='Fine Amount',
        compute='_compute_fine_amount',
        store=True,
        help='Fine amount for overdue return'
    )
    
    # Member type info for reference
    member_type_id = fields.Many2one(
        'library.member.type',
        related='member_id.member_type_id',
        string='Member Type',
        store=True,
        readonly=True
    )
    
    # Email tracking
    due_reminder_sent = fields.Boolean(string='Due Reminder Sent', default=False)
    overdue_reminder_sent = fields.Boolean(string='Overdue Reminder Sent', default=False)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The borrow reference must be unique!'),
    ]

    @api.model
    def create(self, vals):
        """Auto-generate sequence and handle book availability."""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('library.borrow') or 'New'
        
        # Auto-compute due date if not provided
        if 'due_date' not in vals and 'member_id' in vals and 'borrow_date' in vals:
            member = self.env['library.member'].browse(vals['member_id'])
            borrow_date = fields.Date.from_string(vals['borrow_date'])
            vals['due_date'] = fields.Date.to_string(borrow_date + timedelta(days=member.max_loan_days))
        
        record = super(LibraryBorrow, self).create(vals)
        
        # Decrease available copies when borrowed
        if record.state == 'borrowed' and record.book_id.available_copies > 0:
            record.book_id.available_copies -= 1
        
        return record

    def write(self, vals):
        """Handle state transitions and book availability."""
        for record in self:
            old_state = record.state
            result = super(LibraryBorrow, record).write(vals)
            new_state = record.state
            
            # Handle book availability on state change
            if old_state != new_state:
                if old_state in ('draft', 'cancelled') and new_state == 'borrowed':
                    # Book is being borrowed
                    if record.book_id.available_copies > 0:
                        record.book_id.available_copies -= 1
                elif old_state == 'borrowed' and new_state in ('returned', 'cancelled'):
                    # Book is being returned
                    record.book_id.available_copies += 1
                    if new_state == 'returned' and not record.return_date:
                        record.return_date = fields.Date.today()
        
        return super(LibraryBorrow, self).write(vals)

    @api.constrains('member_id', 'book_id', 'state')
    def _check_borrow_constraints(self):
        """Validate borrow limits and book availability."""
        for record in self:
            if record.state == 'borrowed':
                # Check member can borrow
                can_borrow, error_msg = record.member_id.can_borrow_book()
                if not can_borrow:
                    # Allow if this is already an active borrow being updated
                    active_borrows = self.search_count([
                        ('member_id', '=', record.member_id.id),
                        ('state', '=', 'borrowed'),
                        ('id', '!=', record.id)
                    ])
                    if active_borrows >= record.member_id.max_concurrent_loans:
                        raise ValidationError(error_msg)
                
                # Check book availability
                if record.book_id.available_copies < 1:
                    raise ValidationError(f'The book "{record.book_id.name}" is not available for borrowing.')

    @api.constrains('borrow_date', 'due_date', 'return_date')
    def _check_dates(self):
        """Validate date logic."""
        for record in self:
            if record.due_date and record.due_date < record.borrow_date:
                raise ValidationError('Due date cannot be before borrow date.')
            if record.return_date and record.return_date < record.borrow_date:
                raise ValidationError('Return date cannot be before borrow date.')

    @api.depends('borrow_date', 'return_date', 'due_date')
    def _compute_borrow_duration(self):
        """Compute borrow duration."""
        for record in self:
            if record.borrow_date:
                end_date = record.return_date or fields.Date.today()
                delta = end_date - record.borrow_date
                record.borrow_duration = delta.days
            else:
                record.borrow_duration = 0

    @api.depends('due_date', 'return_date', 'state')
    def _compute_overdue_info(self):
        """Compute overdue status and days."""
        today = fields.Date.today()
        for record in self:
            if record.state in ('borrowed', 'overdue') and record.due_date:
                effective_date = record.return_date or today
                if effective_date > record.due_date:
                    record.is_overdue = True
                    delta = effective_date - record.due_date
                    record.overdue_days = delta.days
                else:
                    record.is_overdue = False
                    record.overdue_days = 0
            else:
                record.is_overdue = False
                record.overdue_days = 0

    @api.depends('overdue_days', 'member_type_id')
    def _compute_fine_amount(self):
        """Compute fine amount based on overdue days and member type."""
        for record in self:
            if record.overdue_days > 0 and record.member_type_id:
                record.fine_amount = record.overdue_days * record.member_type_id.fine_per_day
            else:
                record.fine_amount = 0.0

    def action_confirm(self):
        """Confirm and activate the borrow."""
        for record in self:
            if record.state == 'draft':
                record.state = 'borrowed'
                record.message_post(body=f'Loan confirmed for book "{record.book_id.name}"')

    def action_return(self):
        """Mark book as returned."""
        for record in self:
            if record.state in ('borrowed', 'overdue'):
                record.write({
                    'state': 'returned',
                    'return_date': fields.Date.today()
                })
                record.message_post(body=f'Book "{record.book_id.name}" returned')

    def action_cancel(self):
        """Cancel the borrow."""
        for record in self:
            if record.state in ('draft', 'borrowed'):
                record.state = 'cancelled'
                record.message_post(body='Loan cancelled')

    @api.model
    def _cron_update_overdue_status(self):
        """Scheduled action to update overdue loans."""
        today = fields.Date.today()
        overdue_borrows = self.search([
            ('state', '=', 'borrowed'),
            ('due_date', '<', today)
        ])
        
        for borrow in overdue_borrows:
            borrow.write({'state': 'overdue'})
            borrow.message_post(
                body=f'Loan is now overdue by {borrow.overdue_days} days. Fine: {borrow.fine_amount}'
            )
        
        return True

    @api.model
    def _cron_send_due_reminders(self):
        """Send reminders for books due soon (2 days before due date)."""
        from datetime import timedelta
        target_date = fields.Date.today() + timedelta(days=2)
        
        borrows = self.search([
            ('state', '=', 'borrowed'),
            ('due_date', '=', target_date),
            ('due_reminder_sent', '=', False)
        ])
        
        template = self.env.ref('baramej_library_system.mail_template_loan_due_soon', raise_if_not_found=False)
        if template:
            for borrow in borrows:
                if borrow.member_id.email:
                    template.send_mail(borrow.id, force_send=True)
                    borrow.due_reminder_sent = True
        
        return True

    @api.model
    def _cron_send_overdue_reminders(self):
        """Send reminders for overdue books."""
        borrows = self.search([
            ('state', '=', 'overdue'),
            ('overdue_reminder_sent', '=', False)
        ])
        
        template = self.env.ref('baramej_library_system.mail_template_loan_overdue', raise_if_not_found=False)
        if template:
            for borrow in borrows:
                if borrow.member_id.email:
                    template.send_mail(borrow.id, force_send=True)
                    borrow.overdue_reminder_sent = True
        
        return True