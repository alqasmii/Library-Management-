from odoo import models, fields

class LibraryLocation(models.Model):
    _name = 'library.location'
    _description = 'Library Location'

    name = fields.Char(string='Location Name', required=True)
    code = fields.Char(string='Location Code', required=True)
    address = fields.Text(string='Address')
