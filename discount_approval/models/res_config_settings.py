# -*- coding: utf-8 -*-


from odoo import models, fields, api


class ResConfSettings(models.TransientModel):
    """"sale module setting management"""

    _inherit = "res.config.settings"

    discount_limit = fields.Boolean(string="Discount Limit", store=True)
    discount_money = fields.Float(string="Max Limit", config_parameter='discount.discount_money')
    limit = fields.Float(string='limit')

    def set_values(self):
        """"saving the field value in setting part of sale"""

        res = super(ResConfSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('discount.discount_money', self.discount_money)
        self.env['ir.config_parameter'].sudo().set_param('discount.discount_limit', self.discount_limit)
        self.limit = self.env['ir.config_parameter'].get_param('discount.discount_money')
        return res

    @api.model
    def get_values(self):
        """"retrieving the value in setting part of sale"""

        res = super(ResConfSettings, self).get_values()
        sudo = self.env['ir.config_parameter'].sudo()
        res.update(
            discount_money=sudo.get_param('discount.discount_money'),
            discount_limit=sudo.get_param('discount.discount_limit'),
        )
        return res
