from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'

    name = fields.Char(string='Name', required=True)
    member_id = fields.Char(string='Member ID', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    active = fields.Boolean(string='Active', default=True)
    membership_start_date = fields.Date(string='Membership Start Date', default=fields.Date.today)
    membership_end_date = fields.Date(string='Membership End Date')
    membership_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Membership Status', compute='_compute_membership_status', store=True)

    _sql_constraints = [
        ('member_id_unique', 'UNIQUE(member_id)', 'The Member ID must be unique.')
    ]

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError('Invalid email format.')

    @api.depends('membership_start_date', 'membership_end_date')
    def _compute_membership_status(self):
        for record in self:
            today = fields.Date.today()
            if record.membership_end_date and record.membership_end_date < today:
                record.membership_status = 'inactive'
            else:
                record.membership_status = 'active'