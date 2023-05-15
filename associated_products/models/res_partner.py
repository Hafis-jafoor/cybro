# -*- coding: utf-8 -*-


from odoo import models, fields


class ResPartner(models.Model):
    """contact module Management"""

    _inherit = 'res.partner'

    associative_products = fields.Many2many('product.product', string='Products')

