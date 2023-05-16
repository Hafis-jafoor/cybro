# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MenuCategories(models.Model):
    """"list of menu categories"""

    _name = 'menu.categories'
    _description = "menu categories"

    inv_welcome_id = fields.Many2one('event.catering')
    inv_breakfast_id = fields.Many2one('event.catering')
    inv_lunch_id = fields.Many2one('event.catering')
    inv_dinner_id = fields.Many2one('event.catering')
    inv_snacks_id = fields.Many2one('event.catering')
    inv_drinks_id = fields.Many2one('event.catering')
    inv_beverages_id = fields.Many2one('event.catering')
    menu_dish_id = fields.Many2one('event.catering.menu', string='Item')
    menu_dish_uom_id = fields.Many2one('uom.uom', compute='_compute_uom', inverse='_inverse_uom', string='UOM',
                                       store=True)
    menu_dish_quantity = fields.Float(string='Qty', default='1')
    menu_dish_unit_price = fields.Float(compute='_compute_unit_price', inverse="_inverse_price", string='Unit Price',
                                        store=True)
    menu_dish_subtotal = fields.Float(compute='_compute_amount', string='SubTotal', store=True)
    menu_dish_description = fields.Char(string='Description', readonly=False)

    @api.depends('menu_dish_quantity', 'menu_dish_unit_price')
    def _compute_amount(self):
        """"Compute the amount of the menu line"""

        for record in self:
            record.menu_dish_subtotal = record.menu_dish_quantity * record.menu_dish_unit_price

    @api.depends('menu_dish_id')
    def _compute_unit_price(self):
        """"Compute the amount of the unit prize from event catering menu"""

        for record in self:
            record.menu_dish_unit_price = record.menu_dish_id.menu_dish_unit_price

    def _inverse_price(self):
        """"make unit prize editable"""
        pass

    @api.depends('menu_dish_id')
    def _compute_uom(self):
        """"Compute the amount of the uom from event catering menu"""

        for record in self:
            record.menu_dish_uom_id = record.menu_dish_id.menu_dish_uom_id

    def _inverse_uom(self):
        """"make uom editable"""
        pass
