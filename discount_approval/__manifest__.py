{
    'name': 'Discount Approval',
    'version': '16.0.1.0.0',
    'sequence': 11,
    'depends': ['base', 'product', 'sale'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/res_config_settings.xml',
        'views/sale_order.xml',
    ],
}