from odoo import models, fields

class LibraryReview(models.Model):
    _name = 'library.review'
    _description = 'Library Book Review'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    member_id = fields.Many2one('library.member', string='Member', required=True)
    rating = fields.Selection([(str(i), str(i)) for i in range(1, 6)], string='Rating', required=True)
    review = fields.Text(string='Review')
