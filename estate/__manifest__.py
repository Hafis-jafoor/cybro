# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Estate',
    'version': '1.2',
    'summary': 'Estate',
    'sequence': 10,
    'depends': ['base_setup'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'category': 'Real Estate/Brokerage',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
}
