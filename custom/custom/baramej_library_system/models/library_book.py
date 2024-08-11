from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Library Borrow'

    member_id = fields.Many2one('library.member', string='Member', required=True)
    book_id = fields.Many2one('library.book', string='Book', required=True)
    staff_id = fields.Many2one('library.staff', string='Handled By', required=True)
    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.today)
    return_date = fields.Date(string='Return Date')
    state = fields.Selection([
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned')
    ], string='Status', default='borrowed')
    borrow_duration = fields.Integer(string='Duration (days)', compute='_compute_borrow_duration')
    is_overdue = fields.Boolean(string='Is Overdue', compute='_compute_is_overdue')

    @api.constrains('return_date')
    def _check_return_date(self):
        for record in self:
            if record.return_date and record.return_date < record.borrow_date:
                raise ValidationError('Return date cannot be before borrow date.')

    @api.constrains('book_id', 'state')
    def _check_book_availability(self):
        for record in self:
            if record.state == 'borrowed' and record.book_id.available_copies < 1:
                raise ValidationError('The book is not available for borrowing.')

    @api.depends('borrow_date', 'return_date')
    def _compute_borrow_duration(self):
        for record in self:
            if record.borrow_date and record.return_date:
                delta = record.return_date - record.borrow_date
                record.borrow_duration = delta.days
            else:
                record.borrow_duration = 0

    @api.depends('return_date')
    def _compute_is_overdue(self):
        for record in self:
            if record.return_date and record.return_date < fields.Date.today():
                record.is_overdue = True
            else:
                record.is_overdue = False

    @api.model
    def create(self, vals):
        record = super(LibraryBorrow, self).create(vals)
        record.book_id.available_copies -= 1
        return record

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'returned':
            self.book_id.available_copies += 1
        return super(LibraryBorrow, self).write(vals)