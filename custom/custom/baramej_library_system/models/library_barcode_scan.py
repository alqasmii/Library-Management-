# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class LibraryBarcodeScan(models.TransientModel):
    """Wizard for barcode scanning operations (quick checkout/return)."""
    _name = 'library.barcode.scan'
    _description = 'Library Barcode Scanner'

    member_barcode = fields.Char(string='Member Barcode', required=True)
    book_barcode = fields.Char(string='Book Barcode', required=True)
    operation = fields.Selection([
        ('auto', 'Auto Detect'),
        ('borrow', 'Borrow'),
        ('return', 'Return')
    ], string='Operation', default='auto', required=True)
    result_message = fields.Text(string='Result', readonly=True)
    
    def action_process_scan(self):
        """Process the barcode scan and create/close loan."""
        self.ensure_one()
        
        # Find member
        member = self.env['library.member'].search_by_barcode(self.member_barcode)
        if not member:
            raise UserError(f'No member found with barcode: {self.member_barcode}')
        
        # Find book
        book = self.env['library.book'].search_by_barcode(self.book_barcode)
        if not book:
            raise UserError(f'No book found with barcode: {self.book_barcode}')
        
        # Auto-detect operation if needed
        operation = self.operation
        if operation == 'auto':
            # Check if member has this book borrowed
            active_borrow = self.env['library.borrow'].search([
                ('member_id', '=', member.id),
                ('book_id', '=', book.id),
                ('state', 'in', ['borrowed', 'overdue'])
            ], limit=1)
            
            operation = 'return' if active_borrow else 'borrow'
        
        # Process operation
        if operation == 'borrow':
            return self._process_borrow(member, book)
        else:
            return self._process_return(member, book)
    
    def _process_borrow(self, member, book):
        """Create a new borrow record."""
        # Check member can borrow
        can_borrow, error_msg = member.can_borrow_book()
        if not can_borrow:
            raise UserError(error_msg)
        
        # Check book availability
        if book.available_copies < 1:
            raise UserError(f'Book "{book.name}" is not available (0 copies available)')
        
        # Create borrow record
        borrow = self.env['library.borrow'].create({
            'member_id': member.id,
            'book_id': book.id,
            'state': 'borrowed',
        })
        
        message = f'✓ Book borrowed successfully!\n\n'
        message += f'Member: {member.name} ({member.member_id})\n'
        message += f'Book: {book.name}\n'
        message += f'Due Date: {borrow.due_date}\n'
        message += f'Reference: {borrow.name}'
        
        self.result_message = message
        
        return {
            'name': 'Scan Result',
            'type': 'ir.actions.act_window',
            'res_model': 'library.barcode.scan',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def _process_return(self, member, book):
        """Return a borrowed book."""
        # Find active borrow
        borrow = self.env['library.borrow'].search([
            ('member_id', '=', member.id),
            ('book_id', '=', book.id),
            ('state', 'in', ['borrowed', 'overdue'])
        ], limit=1)
        
        if not borrow:
            raise UserError(f'No active loan found for member "{member.name}" and book "{book.name}"')
        
        # Mark as returned
        borrow.action_return()
        
        message = f'✓ Book returned successfully!\n\n'
        message += f'Member: {member.name} ({member.member_id})\n'
        message += f'Book: {book.name}\n'
        message += f'Borrowed: {borrow.borrow_date}\n'
        message += f'Returned: {borrow.return_date}\n'
        
        if borrow.overdue_days > 0:
            message += f'\n⚠ OVERDUE: {borrow.overdue_days} days\n'
            message += f'Fine: ${borrow.fine_amount:.2f}'
        
        self.result_message = message
        
        return {
            'name': 'Scan Result',
            'type': 'ir.actions.act_window',
            'res_model': 'library.barcode.scan',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
