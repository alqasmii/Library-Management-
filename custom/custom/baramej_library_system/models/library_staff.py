from odoo import models, fields

class LibraryStaff(models.Model):
    _name = 'library.staff'
    _description = 'Library Staff'

    name = fields.Char(string='Name', required=True)
    role = fields.Char(string='Role')
    event_ids = fields.One2many('library.event', 'organizer_id', string='Events')