# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import timedelta
from odoo import fields


class TestBorrowLimits(TransactionCase):
    """Test borrow limit validations and member type constraints."""

    def setUp(self):
        super(TestBorrowLimits, self).setUp()
        
        # Create member type
        self.member_type = self.env['library.member.type'].create({
            'name': 'Test Student',
            'code': 'TEST_STU',
            'max_concurrent_loans': 2,
            'max_loan_days': 14,
            'fine_per_day': 0.50,
        })
        
        # Create member
        self.member = self.env['library.member'].create({
            'name': 'Test Member',
            'member_id': 'TEST001',
            'email': 'test@example.com',
            'member_type_id': self.member_type.id,
        })
        
        # Create books
        self.book1 = self.env['library.book'].create({
            'name': 'Test Book 1',
            'isbn': 'TEST-ISBN-001',
            'available_copies': 1,
        })
        
        self.book2 = self.env['library.book'].create({
            'name': 'Test Book 2',
            'isbn': 'TEST-ISBN-002',
            'available_copies': 1,
        })
        
        self.book3 = self.env['library.book'].create({
            'name': 'Test Book 3',
            'isbn': 'TEST-ISBN-003',
            'available_copies': 1,
        })

    def test_member_type_positive_limits(self):
        """Test that member type limits must be positive."""
        with self.assertRaises(ValidationError):
            self.env['library.member.type'].create({
                'name': 'Invalid Type',
                'code': 'INVALID',
                'max_concurrent_loans': 0,
                'max_loan_days': 14,
            })

    def test_borrow_within_limit(self):
        """Test borrowing within member's limit."""
        # First borrow should succeed
        borrow1 = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book1.id,
            'state': 'borrowed',
        })
        self.assertEqual(borrow1.state, 'borrowed')
        self.assertEqual(self.member.active_loan_count, 1)
        
        # Second borrow should succeed (within limit of 2)
        borrow2 = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book2.id,
            'state': 'borrowed',
        })
        self.assertEqual(borrow2.state, 'borrowed')
        self.assertEqual(self.member.active_loan_count, 2)

    def test_borrow_exceeds_limit(self):
        """Test that borrowing beyond limit raises validation error."""
        # Borrow 2 books (at limit)
        self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book1.id,
            'state': 'borrowed',
        })
        self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book2.id,
            'state': 'borrowed',
        })
        
        # Third borrow should fail
        with self.assertRaises(ValidationError):
            self.env['library.borrow'].create({
                'member_id': self.member.id,
                'book_id': self.book3.id,
                'state': 'borrowed',
            })

    def test_book_availability_check(self):
        """Test that unavailable books cannot be borrowed."""
        # Set book to 0 available copies
        self.book1.available_copies = 0
        
        # Try to borrow - should fail
        with self.assertRaises(ValidationError):
            self.env['library.borrow'].create({
                'member_id': self.member.id,
                'book_id': self.book1.id,
                'state': 'borrowed',
            })

    def test_due_date_auto_calculation(self):
        """Test that due date is automatically calculated from member type."""
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book1.id,
            'borrow_date': fields.Date.today(),
        })
        
        expected_due_date = fields.Date.today() + timedelta(days=self.member_type.max_loan_days)
        self.assertEqual(borrow.due_date, expected_due_date)

    def test_return_frees_slot(self):
        """Test that returning a book frees up a borrowing slot."""
        # Borrow 2 books (at limit)
        borrow1 = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book1.id,
            'state': 'borrowed',
        })
        borrow2 = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book2.id,
            'state': 'borrowed',
        })
        
        self.assertEqual(self.member.active_loan_count, 2)
        
        # Return one book
        borrow1.action_return()
        self.assertEqual(self.member.active_loan_count, 1)
        
        # Now should be able to borrow another
        borrow3 = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book3.id,
            'state': 'borrowed',
        })
        self.assertEqual(borrow3.state, 'borrowed')
        self.assertEqual(self.member.active_loan_count, 2)

    def test_inactive_member_cannot_borrow(self):
        """Test that inactive member cannot borrow."""
        self.member.active = False
        
        can_borrow, error_msg = self.member.can_borrow_book()
        self.assertFalse(can_borrow)
        self.assertIn('suspended', error_msg.lower())
