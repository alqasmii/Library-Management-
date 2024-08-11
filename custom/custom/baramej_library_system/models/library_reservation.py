from odoo import models, fields

class LibraryReservation(models.Model):
    _name = 'library.reservation'
    _description = 'Library Book Reservation'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    member_id = fields.Many2one('library.member', string='Member', required=True)
    reservation_date = fields.Date(string='Reservation Date', default=fields.Date.today)
    status = fields.Selection([
        ('reserved', 'Reserved'),
        ('canceled', 'Canceled')
    ], string='Status', default='reserved')
