{
    'name': 'Invoice Multiple Sale Order',
    'version': '16.0.1.0.0',
    'sequence': 7,
    'depends': ['base', 'sale', 'account_payment', 'product'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/account_move.xml',
    ],
}
