from odoo import models, fields

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Library Author'

    name = fields.Char(string='Name', required=True)
    biography = fields.Text(string='Biography')
    book_ids = fields.One2many('library.book', 'author_id', string='Books')
