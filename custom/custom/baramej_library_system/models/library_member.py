# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class LibraryMember(models.Model):
    """Library member with tier/type for borrowing limits."""
    _name = 'library.member'
    _description = 'Library Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, tracking=True)
    member_id = fields.Char(string='Member ID', required=True, copy=False, tracking=True)
    barcode = fields.Char(string='Barcode', copy=False, help='Barcode for quick scanning')
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    address = fields.Text(string='Address')
    active = fields.Boolean(string='Active', default=True, tracking=True)
    
    # Member type/tier
    member_type_id = fields.Many2one(
        'library.member.type',
        string='Member Type',
        required=True,
        tracking=True,
        help='Member tier that defines borrowing limits'
    )
    
    # Membership dates
    membership_start_date = fields.Date(
        string='Membership Start Date',
        default=fields.Date.today,
        required=True,
        tracking=True
    )
    membership_end_date = fields.Date(string='Membership End Date', tracking=True)
    membership_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended')
    ], string='Membership Status', compute='_compute_membership_status', store=True, tracking=True)
    
    # Loan statistics
    borrow_ids = fields.One2many('library.borrow', 'member_id', string='Borrowings')
    active_loan_count = fields.Integer(
        string='Active Loans',
        compute='_compute_loan_stats',
        help='Number of currently borrowed books'
    )
    overdue_loan_count = fields.Integer(
        string='Overdue Loans',
        compute='_compute_loan_stats',
        help='Number of overdue books'
    )
    total_loans = fields.Integer(
        string='Total Loans',
        compute='_compute_loan_stats',
        help='Lifetime loan count'
    )
    total_fines = fields.Float(
        string='Total Fines',
        compute='_compute_total_fines',
        help='Total outstanding fines'
    )
    
    # Computed limits from member type
    max_concurrent_loans = fields.Integer(
        string='Max Concurrent Loans',
        related='member_type_id.max_concurrent_loans',
        readonly=True
    )
    max_loan_days = fields.Integer(
        string='Max Loan Days',
        related='member_type_id.max_loan_days',
        readonly=True
    )

    _sql_constraints = [
        ('member_id_unique', 'UNIQUE(member_id)', 'The Member ID must be unique.'),
        ('barcode_unique', 'UNIQUE(barcode)', 'The Barcode must be unique.'),
    ]

    @api.constrains('email')
    def _check_email_format(self):
        """Validate email format."""
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError('Invalid email format.')

    @api.constrains('membership_start_date', 'membership_end_date')
    def _check_membership_dates(self):
        """Ensure end date is after start date."""
        for record in self:
            if record.membership_end_date and record.membership_end_date < record.membership_start_date:
                raise ValidationError('Membership end date cannot be before start date.')

    @api.depends('membership_start_date', 'membership_end_date', 'active')
    def _compute_membership_status(self):
        """Compute membership status based on dates."""
        today = fields.Date.today()
        for record in self:
            if not record.active:
                record.membership_status = 'suspended'
            elif record.membership_end_date and record.membership_end_date < today:
                record.membership_status = 'inactive'
            else:
                record.membership_status = 'active'

    @api.depends('borrow_ids', 'borrow_ids.state')
    def _compute_loan_stats(self):
        """Compute loan statistics."""
        for record in self:
            borrows = record.borrow_ids
            record.active_loan_count = len(borrows.filtered(lambda b: b.state == 'borrowed'))
            record.overdue_loan_count = len(borrows.filtered(lambda b: b.state == 'overdue'))
            record.total_loans = len(borrows)

    @api.depends('borrow_ids', 'borrow_ids.fine_amount', 'borrow_ids.state')
    def _compute_total_fines(self):
        """Compute total outstanding fines."""
        for record in self:
            overdue_borrows = record.borrow_ids.filtered(lambda b: b.state in ('overdue', 'borrowed'))
            record.total_fines = sum(overdue_borrows.mapped('fine_amount'))

    def can_borrow_book(self):
        """Check if member can borrow more books."""
        self.ensure_one()
        if self.membership_status != 'active':
            return False, f'Member {self.name} has {self.membership_status} membership.'
        if self.active_loan_count >= self.max_concurrent_loans:
            return False, f'Member {self.name} has reached the maximum of {self.max_concurrent_loans} concurrent loans.'
        return True, ''

    @api.model
    def search_by_barcode(self, barcode):
        """Search member by barcode for scanning operations."""
        return self.search([('barcode', '=', barcode)], limit=1)
