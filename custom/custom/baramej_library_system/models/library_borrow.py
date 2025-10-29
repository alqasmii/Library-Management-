# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    """Library book with barcode and availability tracking."""
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Title', required=True, tracking=True)
    barcode = fields.Char(string='Barcode', copy=False, help='Barcode for quick scanning')
    author_id = fields.Many2one('library.author', string='Author', required=True, tracking=True)
    isbn = fields.Char(string='ISBN', tracking=True)
    category_id = fields.Many2one('library.category', string='Category', tracking=True)
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    publication_date = fields.Date(string='Publication Date')
    available_copies = fields.Integer(string='Available Copies', default=1, tracking=True)
    total_copies = fields.Integer(string='Total Copies', compute='_compute_total_copies', store=True)
    pages = fields.Integer(string='Number of Pages')
    language = fields.Char(string='Language')
    review_ids = fields.One2many('library.review', 'book_id', string='Reviews')
    location_id = fields.Many2one('library.location', string='Location')
    borrow_ids = fields.One2many('library.borrow', 'book_id', string='Borrowings')
    
    # Computed availability info
    is_available = fields.Boolean(string='Available', compute='_compute_is_available')
    active_borrow_count = fields.Integer(string='Currently Borrowed', compute='_compute_borrow_stats')

    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'The ISBN must be unique.'),
        ('barcode_unique', 'UNIQUE(barcode)', 'The Barcode must be unique.'),
    ]

    @api.constrains('publication_date')
    def _check_publication_date(self):
        """Ensure publication date is not in the future."""
        for record in self:
            if record.publication_date and record.publication_date > fields.Date.today():
                raise ValidationError('Publication date cannot be in the future.')

    @api.depends('available_copies', 'borrow_ids', 'borrow_ids.state')
    def _compute_total_copies(self):
        """Compute total copies from available + borrowed."""
        for record in self:
            borrowed_copies = len(record.borrow_ids.filtered(lambda b: b.state == 'borrowed'))
            record.total_copies = record.available_copies + borrowed_copies

    @api.depends('available_copies')
    def _compute_is_available(self):
        """Check if book is available for borrowing."""
        for record in self:
            record.is_available = record.available_copies > 0

    @api.depends('borrow_ids', 'borrow_ids.state')
    def _compute_borrow_stats(self):
        """Compute borrow statistics."""
        for record in self:
            record.active_borrow_count = len(record.borrow_ids.filtered(lambda b: b.state == 'borrowed'))

    @api.model
    def search_by_barcode(self, barcode):
        """Search book by barcode for scanning operations."""
        return self.search([('barcode', '=', barcode)], limit=1)