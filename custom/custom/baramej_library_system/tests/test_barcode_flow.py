# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields


class TestBarcodeFlow(TransactionCase):
    """Test barcode scanning operations for checkout and return."""

    def setUp(self):
        super(TestBarcodeFlow, self).setUp()
        
        # Create member type
        self.member_type = self.env['library.member.type'].create({
            'name': 'Test Student',
            'code': 'TEST_STU',
            'max_concurrent_loans': 3,
            'max_loan_days': 14,
            'fine_per_day': 0.50,
        })
        
        # Create member with barcode
        self.member = self.env['library.member'].create({
            'name': 'Test Member',
            'member_id': 'TEST001',
            'barcode': 'MEM001',
            'email': 'test@example.com',
            'member_type_id': self.member_type.id,
        })
        
        # Create book with barcode
        self.book = self.env['library.book'].create({
            'name': 'Test Book',
            'isbn': 'TEST-ISBN-001',
            'barcode': 'BOOK001',
            'available_copies': 1,
        })

    def test_search_member_by_barcode(self):
        """Test searching for member by barcode."""
        found_member = self.env['library.member'].search_by_barcode('MEM001')
        self.assertEqual(found_member.id, self.member.id)
        
        # Test non-existent barcode
        not_found = self.env['library.member'].search_by_barcode('NONEXISTENT')
        self.assertFalse(not_found)

    def test_search_book_by_barcode(self):
        """Test searching for book by barcode."""
        found_book = self.env['library.book'].search_by_barcode('BOOK001')
        self.assertEqual(found_book.id, self.book.id)
        
        # Test non-existent barcode
        not_found = self.env['library.book'].search_by_barcode('NONEXISTENT')
        self.assertFalse(not_found)

    def test_barcode_scan_borrow_auto(self):
        """Test automatic borrow operation via barcode scan."""
        scanner = self.env['library.barcode.scan'].create({
            'member_barcode': 'MEM001',
            'book_barcode': 'BOOK001',
            'operation': 'auto',
        })
        
        # Process scan - should create borrow
        result = scanner.action_process_scan()
        
        # Check that borrow was created
        borrow = self.env['library.borrow'].search([
            ('member_id', '=', self.member.id),
            ('book_id', '=', self.book.id),
            ('state', '=', 'borrowed')
        ])
        
        self.assertEqual(len(borrow), 1)
        self.assertEqual(borrow.state, 'borrowed')
        self.assertEqual(self.book.available_copies, 0)

    def test_barcode_scan_return_auto(self):
        """Test automatic return operation via barcode scan."""
        # Create an active borrow
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'state': 'borrowed',
        })
        
        initial_copies = self.book.available_copies
        
        # Scan to return
        scanner = self.env['library.barcode.scan'].create({
            'member_barcode': 'MEM001',
            'book_barcode': 'BOOK001',
            'operation': 'auto',
        })
        
        result = scanner.action_process_scan()
        
        # Check that book was returned
        self.assertEqual(borrow.state, 'returned')
        self.assertIsNotNone(borrow.return_date)
        self.assertEqual(self.book.available_copies, initial_copies + 1)

    def test_barcode_scan_explicit_borrow(self):
        """Test explicit borrow operation via barcode scan."""
        scanner = self.env['library.barcode.scan'].create({
            'member_barcode': 'MEM001',
            'book_barcode': 'BOOK001',
            'operation': 'borrow',
        })
        
        result = scanner.action_process_scan()
        
        borrow = self.env['library.borrow'].search([
            ('member_id', '=', self.member.id),
            ('book_id', '=', self.book.id),
            ('state', '=', 'borrowed')
        ])
        
        self.assertEqual(len(borrow), 1)

    def test_barcode_scan_explicit_return(self):
        """Test explicit return operation via barcode scan."""
        # Create an active borrow
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'state': 'borrowed',
        })
        
        scanner = self.env['library.barcode.scan'].create({
            'member_barcode': 'MEM001',
            'book_barcode': 'BOOK001',
            'operation': 'return',
        })
        
        result = scanner.action_process_scan()
        
        self.assertEqual(borrow.state, 'returned')

    def test_barcode_scan_invalid_member(self):
        """Test that scanning invalid member barcode raises error."""
        scanner = self.env['library.barcode.scan'].create({
            'member_barcode': 'INVALID',
            'book_barcode': 'BOOK001',
            'operation': 'auto',
        })
        
        with self.assertRaises(UserError):
            scanner.action_process_scan()

    def test_barcode_scan_invalid_book(self):
        """Test that scanning invalid book barcode raises error."""
        scanner = self.env['library.barcode.scan'].create({
            'member_barcode': 'MEM001',
            'book_barcode': 'INVALID',
            'operation': 'auto',
        })
        
        with self.assertRaises(UserError):
            scanner.action_process_scan()

    def test_barcode_scan_unavailable_book(self):
        """Test that scanning unavailable book raises error."""
        self.book.available_copies = 0
        
        scanner = self.env['library.barcode.scan'].create({
            'member_barcode': 'MEM001',
            'book_barcode': 'BOOK001',
            'operation': 'borrow',
        })
        
        with self.assertRaises(UserError):
            scanner.action_process_scan()

    def test_barcode_scan_no_active_loan_return(self):
        """Test that attempting to return non-borrowed book raises error."""
        scanner = self.env['library.barcode.scan'].create({
            'member_barcode': 'MEM001',
            'book_barcode': 'BOOK001',
            'operation': 'return',
        })
        
        with self.assertRaises(UserError):
            scanner.action_process_scan()

    def test_barcode_scan_member_limit(self):
        """Test that barcode scan respects member borrowing limits."""
        # Set member type to 1 max loan
        self.member_type.max_concurrent_loans = 1
        
        # Create one active borrow
        self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'state': 'borrowed',
        })
        
        # Try to borrow another book
        book2 = self.env['library.book'].create({
            'name': 'Test Book 2',
            'isbn': 'TEST-ISBN-002',
            'barcode': 'BOOK002',
            'available_copies': 1,
        })
        
        scanner = self.env['library.barcode.scan'].create({
            'member_barcode': 'MEM001',
            'book_barcode': 'BOOK002',
            'operation': 'borrow',
        })
        
        with self.assertRaises(UserError):
            scanner.action_process_scan()

    def test_barcode_unique_constraints(self):
        """Test that barcodes must be unique."""
        from odoo.exceptions import ValidationError
        
        # Try to create member with duplicate barcode
        with self.assertRaises(Exception):  # Could be IntegrityError or ValidationError
            self.env['library.member'].create({
                'name': 'Duplicate Member',
                'member_id': 'TEST002',
                'barcode': 'MEM001',  # Duplicate
                'member_type_id': self.member_type.id,
            })
        
        # Try to create book with duplicate barcode
        with self.assertRaises(Exception):
            self.env['library.book'].create({
                'name': 'Duplicate Book',
                'isbn': 'TEST-ISBN-002',
                'barcode': 'BOOK001',  # Duplicate
                'available_copies': 1,
            })
