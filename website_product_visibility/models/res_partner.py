# -*- coding: utf-8 -*-


from odoo import fields, models


class ResPartner(models.Model):
    """contact module Management"""
    _inherit = 'res.partner'

    p_product_ids = fields.Many2many('product.product', string='Website Products')
    p_category_ids = fields.Many2many('product.public.category', string='Website Products Category')
