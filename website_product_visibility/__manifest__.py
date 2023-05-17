{
    'name': 'Website Product Visibility',
    'version': '16.0.1.0.0',
    'sequence': 5,
    'depends': ['base', 'product', 'sale', 'contacts', 'website_sale'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/res_partner.xml',
    ],
}
