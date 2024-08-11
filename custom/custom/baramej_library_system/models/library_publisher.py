from odoo import models, fields

class LibraryPublisher(models.Model):
    _name = 'library.publisher'
    _description = 'Library Publisher'

    name = fields.Char(string='Publisher Name', required=True)
    address = fields.Text(string='Address')
    book_ids = fields.One2many('library.book', 'publisher_id', string='Books')
