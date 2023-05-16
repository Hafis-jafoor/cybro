# -*- coding: utf-8 -*-


from odoo import api, fields, models


class EventServicesLines(models.Model):
    """"event services lines"""

    _name = 'event.services.lines'
    _description = "event services Lines"

    order_id = fields.Many2one(
        comodel_name='event.services',
        string="Order Reference")
    name_description = fields.Text(
        string="Description")
    product_uom_qty = fields.Float(
        string="Quantity")
    price_unit = fields.Float(
        string="Unit Price")
    service_description_subtotal = fields.Float(compute='_compute_amount', string='SubTotal')

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_amount(self):
        """"Compute the amount of the service line"""

        for record in self:
            record.service_description_subtotal = record.product_uom_qty * record.price_unit



