# -*- coding: utf-8 -*-


from odoo import models, api


class SaleOrder(models.Model):
    """"sale order management"""

    _inherit = 'sale.order'

    def merge_duplicate_product_lines(self, res):
        """"merging the orderliness for same product and unit price"""

        for line in res.order_line:
            if line.id in res.order_line.ids:
                line_ids = res.order_line.filtered(lambda m: m.product_id.id == line.product_id.id and
                                                             m.price_unit == line.price_unit)
                quantity = 0
                for qty in line_ids:
                    quantity += qty.product_uom_qty
                if quantity > 1:
                    line_ids[0].write({'product_uom_qty': quantity,
                                       'order_id': line_ids[0].order_id.id})
                    line_ids[1:].unlink()

    @api.model
    def create(self, vals):
        """"supering the merging function"""

        res = super(SaleOrder, self).create(vals)
        res.merge_duplicate_product_lines(res)
        return res

    def write(self, vals):
        """writing the merging function"""

        res = super(SaleOrder, self).write(vals)
        self.merge_duplicate_product_lines(self)
        return res

