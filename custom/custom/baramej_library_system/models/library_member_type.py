# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryMemberType(models.Model):
    """Member type/tier defining borrowing limits and privileges."""
    _name = 'library.member.type'
    _description = 'Library Member Type'
    _order = 'sequence, name'

    name = fields.Char(string='Type Name', required=True, translate=True)
    code = fields.Char(string='Code', required=True, help='Unique code for this member type')
    sequence = fields.Integer(string='Sequence', default=10)
    max_concurrent_loans = fields.Integer(
        string='Max Concurrent Loans',
        default=3,
        required=True,
        help='Maximum number of books a member can borrow at the same time'
    )
    max_loan_days = fields.Integer(
        string='Max Loan Days',
        default=14,
        required=True,
        help='Maximum number of days a member can keep a book'
    )
    fine_per_day = fields.Float(
        string='Fine per Day',
        default=0.5,
        help='Daily fine amount for overdue books'
    )
    active = fields.Boolean(string='Active', default=True)
    member_ids = fields.One2many('library.member', 'member_type_id', string='Members')
    member_count = fields.Integer(string='Member Count', compute='_compute_member_count')
    color = fields.Integer(string='Color Index')
    description = fields.Text(string='Description', translate=True)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'The member type code must be unique!'),
    ]

    @api.constrains('max_concurrent_loans', 'max_loan_days')
    def _check_positive_values(self):
        """Ensure limits are positive."""
        for record in self:
            if record.max_concurrent_loans <= 0:
                raise ValidationError('Maximum concurrent loans must be greater than zero.')
            if record.max_loan_days <= 0:
                raise ValidationError('Maximum loan days must be greater than zero.')

    @api.depends('member_ids')
    def _compute_member_count(self):
        """Compute the number of members for this type."""
        for record in self:
            record.member_count = len(record.member_ids)

    def name_get(self):
        """Display name with code."""
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result
