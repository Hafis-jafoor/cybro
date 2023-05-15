# -*- coding: utf-8 -*-


from odoo import models, fields, api


class AccountMove(models.Model):
    """contact module Management"""

    _inherit = 'account.move'

    sale_orders_ids = fields.Many2many('sale.order', string='Sale Orders')

    def generate_order_lines(self):
        """"generate order lines"""

        for items in self.invoice_line_ids:
            items.unlink()
        order_lines = []
        ref_source = []
        for record in self.sale_orders_ids:
            ref_source.append(record.name)
            for i in record.order_line:
                order_lines.append(fields.Command.create({
                    'product_id': i.product_id.id,
                    'name': i.name,
                    'quantity': i.product_uom_qty,
                    'price_unit': i.price_unit,
                    'price_subtotal': i.price_subtotal,
                }))

        self.invoice_line_ids = order_lines
        self.invoice_origin = ",".join(ref_source)

    def action_post(self):
        """"confirm button for invoicing supering"""

        res = super(AccountMove, self).action_post()
        for record in self.sale_orders_ids:
            record.invoice_ids = [fields.Command.link(self.id)]
            # record.invoice_count = len(record.invoice_ids)
            # print("---->",record.read())
            record.action_confirm()
            record.invoice_status = "invoiced"
        return res
