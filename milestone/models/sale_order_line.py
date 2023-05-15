# -*- coding: utf-8 -*-


from odoo import models, fields, api


class SaleOrderLine(models.Model):
    """"sale order lines management"""

    _inherit = 'sale.order.line'

    milestone_no = fields.Integer(string='milestone', default=1)



