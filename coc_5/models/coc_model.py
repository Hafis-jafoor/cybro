# -*- coding: utf-8 -*-


from odoo import models, fields, api


class CocModel(models.Model):
    """coc 5 project testing"""

    _name = "coc.model"

    resistence = fields.Selection(selection=[('pass', 'Pass'), ('fail', 'Fail')], string='Resistence')
