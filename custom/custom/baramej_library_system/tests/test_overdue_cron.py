# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from datetime import timedelta
from odoo import fields


class TestOverdueCron(TransactionCase):
    """Test overdue cron job and automatic status updates."""

    def setUp(self):
        super(TestOverdueCron, self).setUp()
        
        # Create member type
        self.member_type = self.env['library.member.type'].create({
            'name': 'Test Student',
            'code': 'TEST_STU',
            'max_concurrent_loans': 3,
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
        
        # Create book
        self.book = self.env['library.book'].create({
            'name': 'Test Book',
            'isbn': 'TEST-ISBN-001',
            'available_copies': 1,
        })

    def test_overdue_status_transition(self):
        """Test that borrowed loans become overdue after due date."""
        # Create borrowed loan with past due date
        past_due_date = fields.Date.today() - timedelta(days=5)
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=20),
            'due_date': past_due_date,
            'state': 'borrowed',
        })
        
        self.assertEqual(borrow.state, 'borrowed')
        self.assertTrue(borrow.is_overdue)
        self.assertEqual(borrow.overdue_days, 5)
        
        # Run cron job
        self.env['library.borrow']._cron_update_overdue_status()
        
        # Check that state changed to overdue
        self.assertEqual(borrow.state, 'overdue')

    def test_overdue_days_calculation(self):
        """Test that overdue days are calculated correctly."""
        past_due_date = fields.Date.today() - timedelta(days=10)
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=25),
            'due_date': past_due_date,
            'state': 'overdue',
        })
        
        self.assertEqual(borrow.overdue_days, 10)

    def test_fine_calculation(self):
        """Test that fines are calculated based on overdue days and member type."""
        past_due_date = fields.Date.today() - timedelta(days=7)
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=22),
            'due_date': past_due_date,
            'state': 'overdue',
        })
        
        expected_fine = 7 * self.member_type.fine_per_day
        self.assertEqual(borrow.fine_amount, expected_fine)

    def test_not_overdue_stays_borrowed(self):
        """Test that not-overdue loans stay as borrowed."""
        future_due_date = fields.Date.today() + timedelta(days=5)
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=9),
            'due_date': future_due_date,
            'state': 'borrowed',
        })
        
        self.assertEqual(borrow.state, 'borrowed')
        self.assertFalse(borrow.is_overdue)
        self.assertEqual(borrow.overdue_days, 0)
        
        # Run cron job
        self.env['library.borrow']._cron_update_overdue_status()
        
        # Should still be borrowed
        self.assertEqual(borrow.state, 'borrowed')

    def test_returned_book_fine_frozen(self):
        """Test that fine is frozen when book is returned late."""
        past_due_date = fields.Date.today() - timedelta(days=10)
        return_date = fields.Date.today() - timedelta(days=3)
        
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=25),
            'due_date': past_due_date,
            'return_date': return_date,
            'state': 'returned',
        })
        
        # Fine should be based on days between due date and return date (7 days)
        expected_fine = 7 * self.member_type.fine_per_day
        self.assertEqual(borrow.fine_amount, expected_fine)

    def test_cron_batch_update(self):
        """Test that cron updates multiple overdue loans."""
        # Create multiple borrowed loans with past due dates
        past_due_date = fields.Date.today() - timedelta(days=3)
        
        borrow1 = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=18),
            'due_date': past_due_date,
            'state': 'borrowed',
        })
        
        book2 = self.env['library.book'].create({
            'name': 'Test Book 2',
            'isbn': 'TEST-ISBN-002',
            'available_copies': 1,
        })
        
        borrow2 = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': book2.id,
            'borrow_date': fields.Date.today() - timedelta(days=20),
            'due_date': past_due_date,
            'state': 'borrowed',
        })
        
        # Run cron
        self.env['library.borrow']._cron_update_overdue_status()
        
        # Both should be overdue
        self.assertEqual(borrow1.state, 'overdue')
        self.assertEqual(borrow2.state, 'overdue')
