# -*- coding: utf-8 -*-


from odoo import models, fields


class EventTypes(models.Model):
    """"event types classification"""
    _name = "event.types"
    _description = "events"

    name = fields.Char(string='Name', required=True)
    code = fields.Integer(string='Code')
    image = fields.Image(string='Image')


