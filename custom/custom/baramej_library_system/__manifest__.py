{
    'name': 'Baramej Library System',
    'version': '1.0',
    'category': 'Library',
    'summary': 'Manage library books, members, and borrowings',
    'author': 'Call Me Adnan',
    'website': 'https://baramej.io',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_borrow_views.xml',
        'views/library_member_views.xml',
        'views/library_event_views.xml',
        'views/library_reservation_views.xml',
        'views/menus.xml',
        'data/library_actions.xml',
    ],
    'installable': True,
    'application': True,
}
