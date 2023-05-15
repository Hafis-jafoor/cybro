# -*- coding: utf-8 -*-


from odoo import models, fields, api


class SaleOrder(models.Model):
    """"sale order management"""

    _inherit = 'sale.order'

    approval_ok = fields.Boolean(string='approval')
    state = fields.Selection(selection_add=[('approve', 'APPROVE'), ('sent',)])

    @api.onchange('order_line')
    def _onchange_discount_limit(self):
        """"getting the discount limit"""
        data = []
        for record in self.order_line:
            prize = record.product_uom_qty * record.price_unit
            prize_discount = prize * (record.discount / 100)
            # difference = 0
            val = 0
            if record.discount != 0:
                total_prize = prize + prize_discount
                difference = total_prize - prize
                data.append(difference)
                for i in data:
                    val += i
            discount_money = int(float(record.env['ir.config_parameter'].get_param('discount.discount_money')))
            if val > discount_money:
                self.approval_ok = True
            else:
                self.approval_ok = False

    def action_confirm(self):
        """"confirm button supering"""

        res = super(SaleOrder, self).action_confirm()
        if self.approval_ok:
            self.state = 'approve'
        return res

    def approve_button(self):
        """"change the state to approve if limit exceeds"""

        self.state = "sale"

#
