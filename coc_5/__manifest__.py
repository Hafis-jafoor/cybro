{
    'name': 'COC 5',
    'version': '16.0.1.0.0',
    'sequence': 30,
    'depends': ['base', 'mail', 'account_payment'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/coc_model.xml',
    ],
}
