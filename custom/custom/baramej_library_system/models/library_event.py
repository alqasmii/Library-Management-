from odoo import models, fields

class LibraryEvent(models.Model):
    _name = 'library.event'
    _description = 'Library Event'

    name = fields.Char(string='Event Name', required=True)
    event_date = fields.Date(string='Event Date', required=True)
    description = fields.Text(string='Description')
    location = fields.Char(string='Location')
    organizer_id = fields.Many2one('library.staff', string='Organizer')
    book_id = fields.Many2one('library.book', string='Book')
