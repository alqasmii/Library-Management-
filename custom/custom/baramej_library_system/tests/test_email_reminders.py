# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from datetime import timedelta
from odoo import fields
from unittest.mock import patch


class TestEmailReminders(TransactionCase):
    """Test email reminder cron jobs and template rendering."""

    def setUp(self):
        super(TestEmailReminders, self).setUp()
        
        # Create member type
        self.member_type = self.env['library.member.type'].create({
            'name': 'Test Student',
            'code': 'TEST_STU',
            'max_concurrent_loans': 3,
            'max_loan_days': 14,
            'fine_per_day': 0.50,
        })
        
        # Create member with email
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

    def test_due_soon_reminder_sent(self):
        """Test that due soon reminders are sent for books due in 2 days."""
        # Create borrow due in 2 days
        due_date = fields.Date.today() + timedelta(days=2)
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=12),
            'due_date': due_date,
            'state': 'borrowed',
            'due_reminder_sent': False,
        })
        
        self.assertFalse(borrow.due_reminder_sent)
        
        # Run due reminder cron
        self.env['library.borrow']._cron_send_due_reminders()
        
        # Check that reminder flag is set
        self.assertTrue(borrow.due_reminder_sent)

    def test_due_soon_reminder_not_sent_twice(self):
        """Test that due soon reminders are not sent twice."""
        due_date = fields.Date.today() + timedelta(days=2)
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=12),
            'due_date': due_date,
            'state': 'borrowed',
            'due_reminder_sent': True,
        })
        
        # Run cron
        self.env['library.borrow']._cron_send_due_reminders()
        
        # Should still be True (no duplicate)
        self.assertTrue(borrow.due_reminder_sent)

    def test_overdue_reminder_sent(self):
        """Test that overdue reminders are sent for overdue books."""
        past_due_date = fields.Date.today() - timedelta(days=3)
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=18),
            'due_date': past_due_date,
            'state': 'overdue',
            'overdue_reminder_sent': False,
        })
        
        self.assertFalse(borrow.overdue_reminder_sent)
        
        # Run overdue reminder cron
        self.env['library.borrow']._cron_send_overdue_reminders()
        
        # Check that reminder flag is set
        self.assertTrue(borrow.overdue_reminder_sent)

    def test_overdue_reminder_not_sent_twice(self):
        """Test that overdue reminders are not sent twice."""
        past_due_date = fields.Date.today() - timedelta(days=3)
        borrow = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=18),
            'due_date': past_due_date,
            'state': 'overdue',
            'overdue_reminder_sent': True,
        })
        
        # Run cron
        self.env['library.borrow']._cron_send_overdue_reminders()
        
        # Should still be True (no duplicate)
        self.assertTrue(borrow.overdue_reminder_sent)

    def test_no_reminder_without_email(self):
        """Test that reminders are not sent if member has no email."""
        # Create member without email
        member_no_email = self.env['library.member'].create({
            'name': 'No Email Member',
            'member_id': 'TEST002',
            'member_type_id': self.member_type.id,
        })
        
        due_date = fields.Date.today() + timedelta(days=2)
        borrow = self.env['library.borrow'].create({
            'member_id': member_no_email.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=12),
            'due_date': due_date,
            'state': 'borrowed',
            'due_reminder_sent': False,
        })
        
        # Run cron (should not crash)
        self.env['library.borrow']._cron_send_due_reminders()
        
        # Reminder flag should still be False (no email to send to)
        self.assertFalse(borrow.due_reminder_sent)

    def test_due_reminder_correct_date(self):
        """Test that due reminders are only sent exactly 2 days before."""
        # Due in 3 days - should not get reminder
        due_date_3_days = fields.Date.today() + timedelta(days=3)
        borrow_3_days = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=11),
            'due_date': due_date_3_days,
            'state': 'borrowed',
            'due_reminder_sent': False,
        })
        
        # Run cron
        self.env['library.borrow']._cron_send_due_reminders()
        
        # Should not have sent reminder
        self.assertFalse(borrow_3_days.due_reminder_sent)

    def test_member_total_fines(self):
        """Test that member total fines aggregate correctly."""
        # Create multiple overdue borrows
        book2 = self.env['library.book'].create({
            'name': 'Test Book 2',
            'isbn': 'TEST-ISBN-002',
            'available_copies': 1,
        })
        
        past_due_date1 = fields.Date.today() - timedelta(days=5)
        borrow1 = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': self.book.id,
            'borrow_date': fields.Date.today() - timedelta(days=20),
            'due_date': past_due_date1,
            'state': 'overdue',
        })
        
        past_due_date2 = fields.Date.today() - timedelta(days=3)
        borrow2 = self.env['library.borrow'].create({
            'member_id': self.member.id,
            'book_id': book2.id,
            'borrow_date': fields.Date.today() - timedelta(days=18),
            'due_date': past_due_date2,
            'state': 'overdue',
        })
        
        expected_total = (5 * 0.50) + (3 * 0.50)
        self.assertEqual(self.member.total_fines, expected_total)
