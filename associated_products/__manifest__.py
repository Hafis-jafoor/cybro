{
    'name': 'Associated Products',
    'version': '16.0.1.0.0',
    'sequence': 10,
    'depends': ['base', 'product', 'sale'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/res_partner.xml',
        'views/sale_order.xml',
    ],
}
