# -*- coding: utf-8 -*-


from odoo import models, fields, api


class EventServices(models.Model):
    """"event services """

    _name = "event.services"
    _description = "event services"

    name = fields.Char(string="Name", required=True)
    responsible_person_id = fields.Many2one('res.users', string="Responsible person")
    order_line_ids = fields.One2many(comodel_name='event.services.lines', inverse_name='order_id', string="Order Lines")
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    service_total = fields.Monetary(compute='_compute_amount', string='TOTAL')

    @api.depends('order_line_ids')
    def _compute_amount(self):
        """"Compute the total of  service lines"""

        for record in self:
            record.service_total = 0
            for i in record.order_line_ids:
                record.service_total += i.service_description_subtotal

