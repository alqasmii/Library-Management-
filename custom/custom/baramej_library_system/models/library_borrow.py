from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    author_id = fields.Many2one('library.author', string='Author', required=True)
    isbn = fields.Char(string='ISBN')
    category_id = fields.Many2one('library.category', string='Category')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    publication_date = fields.Date(string='Publication Date')
    available_copies = fields.Integer(string='Available Copies', default=1)
    total_copies = fields.Integer(string='Total Copies', compute='_compute_total_copies')
    pages = fields.Integer(string='Number of Pages')
    language = fields.Char(string='Language')
    review_ids = fields.One2many('library.review', 'book_id', string='Reviews')
    location_id = fields.Many2one('library.location', string='Location')

    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'The ISBN must be unique.')
    ]

    @api.constrains('publication_date')
    def _check_publication_date(self):
        for record in self:
            if record.publication_date and record.publication_date > fields.Date.today():
                raise ValidationError('Publication date cannot be in the future.')

    @api.depends('available_copies')
    def _compute_total_copies(self):
        for record in self:
            borrowed_copies = 0
            record.total_copies = record.available_copies + borrowed_copies