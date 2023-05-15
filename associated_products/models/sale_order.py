# -*- coding: utf-8 -*-


from odoo import models, fields, api


class SaleOrder(models.Model):
    """Sale Order Management"""

    _inherit = 'sale.order'

    products_ok = fields.Boolean(string='Products')

    @api.onchange('products_ok')
    def _onchange_products_ok(self):
        """"orderliness automated by customer"""

        order_lines = []
        for record in self:
            if record.products_ok:
                lines = record.partner_id.associative_products
                for i in lines:
                    order_lines.append(fields.Command.create({
                        'product_template_id': i.product_tmpl_id,
                        'order_id': self.id,
                        'product_id': i.id,
                        'name': i.name,
                        'customer_lead': 0,
                        'product_uom_qty': 1,
                        'price_unit': i.standard_price,
                    }))
                # val = record.partner_id.associative_products.ids print(val) for k in val: res =
                # record.order_line._origin.search([('product_id', '=', k), ('order_id', '=', self._origin.id)])
                # print(res) if not res:
                record.order_line = order_lines
            else:
                val = record.partner_id.associative_products.ids
                # if val:
                for k in val:
                        record.order_line._origin.search(
                            [('product_id', '=', k), ('order_id', '=', self._origin.id)]).unlink()
