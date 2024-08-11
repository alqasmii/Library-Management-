from odoo import models, fields

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Library Category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
    book_ids = fields.One2many('library.book', 'category_id', string='Books')
