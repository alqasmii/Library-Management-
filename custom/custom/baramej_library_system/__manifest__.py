{
    'name': 'Library Management System v2.0',
    'version': '2.0.0',
    'category': 'Library',
    'summary': 'Complete library management with borrow limits, overdue tracking, email reminders, barcode scanning, and reporting',
    'description': """
        Library Management System v2.0
        ===============================
        
        Features:
        ---------
        * Member tiers with configurable borrow limits
        * Automatic overdue detection and flagging
        * Email reminders for due and overdue books
        * Barcode scanning for quick checkout/return
        * Comprehensive reporting dashboard with KPIs
        * Multi-user security with librarian and member roles
        * Full test coverage
    """,
    'author': 'Call Me Adnan',
    'website': 'https://baramej.io',
    'depends': ['base', 'mail', 'barcodes'],
    'data': [
        # Security
        'security/library_security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/library_member_type_data.xml',
        'data/library_settings_data.xml',
        'data/mail_templates.xml',
        'data/ir_cron.xml',
        
        # Views
        'views/library_member_type_views.xml',
        'views/library_book_views.xml',
        'views/library_member_views.xml',
        'views/library_borrow_views.xml',
        'views/library_event_views.xml',
        'views/library_reservation_views.xml',
        'views/library_barcode_views.xml',
        'views/library_dashboard_views.xml',
        'views/menus.xml',
        'data/library_actions.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'baramej_library_system/static/src/js/barcode_scanner.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
