# -*- coding: utf-8 -*-


from odoo import fields, models


class EventCateringMenu(models.Model):
    """"event catering menu management"""

    _name = "event.catering.menu"
    _description = "event catering menu"
    _rec_name = 'menu_dish_name'

    menu_dish_name = fields.Char(string='Dish Name', required=True)
    menu_category = fields.Selection(
        string='Category Type',
        selection=[('welcome_drink', 'Welcome Drink'), ('break_fast', 'Break Fast'), ('lunch', 'Lunch'),
                   ('dinner', 'Dinner'), ('snacks', 'Snacks'), ('drinks', 'Drinks'), ('beverages', 'Beverages')],
        help="category Type is used to separate different types", required=True)
    menu_dish_image = fields.Image(string='Image')
    menu_dish_uom_id = fields.Many2one('uom.uom', string='UOM', default=1)
    menu_dish_unit_price = fields.Float(string='Unit Price')


