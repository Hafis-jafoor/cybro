# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class EventCatering(models.Model):
    """"event catering services"""

    _name = "event.catering"
    _description = "event catering"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "reference_no"

    reference_no = fields.Char(readonly=True, default=lambda self: _('New'), store=True)
    event_name_id = fields.Many2one('event.bookings', string='Event', required=True)
    event_date = fields.Date(related='event_name_id.booking_date', string='Event Date')
    start_date = fields.Datetime(related='event_name_id.begin_date', string='Event Start Date')
    end_date = fields.Datetime(related='event_name_id.end_date', string='Event End Date')
    guests_count = fields.Integer(string='Guest Count')
    sequence_number = fields.Integer(string='Sequence')
    welcome_drink_ok = fields.Boolean(string='Welcome Drink')
    break_fast_ok = fields.Boolean(string='Break Fast')
    lunch_ok = fields.Boolean(string='Lunch')
    dinner_ok = fields.Boolean(string=' Dinner')
    snacks_ok = fields.Boolean(string='Snacks')
    drinks_ok = fields.Boolean(string='Drinks')
    beverages_ok = fields.Boolean(string='Beverages')
    welcome_drink_ids = fields.One2many(comodel_name='menu.categories', inverse_name='inv_welcome_id')
    break_fast_ids = fields.One2many(comodel_name='menu.categories', inverse_name='inv_breakfast_id')
    lunch_ids = fields.One2many(comodel_name='menu.categories', inverse_name='inv_lunch_id')
    dinner_ids = fields.One2many(comodel_name='menu.categories', inverse_name='inv_dinner_id')
    snacks_ids = fields.One2many(comodel_name='menu.categories', inverse_name='inv_snacks_id')
    drinks_ids = fields.One2many(comodel_name='menu.categories', inverse_name='inv_drinks_id')
    beverages_ids = fields.One2many(comodel_name='menu.categories', inverse_name='inv_beverages_id')
    menu_catering_welcome_total = fields.Float(compute='_compute_welcome_amount', string='Total', store=True)
    menu_catering_breakfast_total = fields.Float(compute='_compute_breakfast_amount', string='Total', store=True)
    menu_catering_lunch_total = fields.Float(compute='_compute_lunch_amount', string='Total', store=True)
    menu_catering_dinner_total = fields.Float(compute='_compute_dinner_amount', string='Total', store=True)
    menu_catering_snacks_total = fields.Float(compute='_compute_snacks_amount', string='Total', store=True)
    menu_catering_drinks_total = fields.Float(compute='_compute_drinks_amount', string='Total', store=True)
    menu_catering_beverages_total = fields.Float(compute='_compute_beverages_amount', string='Total', store=True)
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    menu_catering_total = fields.Monetary(compute='_compute_total_amount', string='TOTAL', store=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('delivered', 'Delivered')],
                             string='status', default='draft')
    invoice_id = fields.Many2one(related='event_name_id.invoice_id')

    @api.depends('welcome_drink_ids', 'welcome_drink_ok')
    def _compute_welcome_amount(self):
        """"Compute the total of  welcome drink lines"""

        for record in self:
            record.menu_catering_welcome_total = 0
            if record.welcome_drink_ok:
                record.menu_catering_welcome_total = sum(record.welcome_drink_ids.mapped('menu_dish_subtotal'))
            else:
                record.welcome_drink_ids = [fields.Command.clear()]

    @api.depends('break_fast_ids', 'break_fast_ok')
    def _compute_breakfast_amount(self):
        """"Compute the total of  break fast lines"""

        for record in self:
            record.menu_catering_breakfast_total = 0
            if record.break_fast_ok:
                record.menu_catering_breakfast_total = sum(record.break_fast_ids.mapped('menu_dish_subtotal'))
            else:
                record.break_fast_ids = [fields.Command.clear()]

    @api.depends('lunch_ids', 'lunch_ok')
    def _compute_lunch_amount(self):
        """"Compute the total of  lunch lines"""

        for record in self:
            record.menu_catering_lunch_total = 0
            if record.lunch_ok:
                record.menu_catering_lunch_total = sum(record.lunch_ids.mapped('menu_dish_subtotal'))
            else:
                record.lunch_ids = [fields.Command.clear()]

    @api.depends('dinner_ids', 'dinner_ok')
    def _compute_dinner_amount(self):
        """"Compute the total of dinner lines"""

        for record in self:
            record.menu_catering_dinner_total = 0
            if record.dinner_ok:
                record.menu_catering_dinner_total = sum(record.dinner_ids.mapped('menu_dish_subtotal'))
            else:
                record.dinner_ids = [fields.Command.clear()]

    @api.depends('snacks_ids', 'snacks_ok')
    def _compute_snacks_amount(self):
        """"Compute the total of snacks lines"""

        for record in self:
            record.menu_catering_snacks_total = 0
            if record.snacks_ok:
                record.menu_catering_snacks_total = sum(record.snacks_ids.mapped('menu_dish_subtotal'))
            else:
                record.snacks_ids = [fields.Command.clear()]

    @api.depends('drinks_ids', 'drinks_ok')
    def _compute_drinks_amount(self):
        """"Compute the total of drinks lines"""

        for record in self:
            record.menu_catering_drinks_total = 0
            if record.drinks_ok:
                record.menu_catering_drinks_total = sum(record.drinks_ids.mapped('menu_dish_subtotal'))
            else:
                record.drinks_ids = [fields.Command.clear()]

    @api.depends('beverages_ids', 'beverages_ok')
    def _compute_beverages_amount(self):
        """"Compute the total of beverages lines"""

        for record in self:
            record.menu_catering_beverages_total = 0
            if record.beverages_ok:
                record.menu_catering_beverages_total = sum(record.beverages_ids.mapped('menu_dish_subtotal'))
            else:
                record.beverages_ids = [fields.Command.clear()]

    @api.depends('menu_catering_welcome_total', 'menu_catering_breakfast_total', 'menu_catering_lunch_total',
                 'menu_catering_dinner_total', 'menu_catering_snacks_total', 'menu_catering_drinks_total',
                 'menu_catering_beverages_total')
    def _compute_total_amount(self):
        """"Compute the total of category page"""

        for record in self:
            record.menu_catering_total = record.menu_catering_welcome_total + record.menu_catering_breakfast_total \
                                         + record.menu_catering_lunch_total + record.menu_catering_dinner_total \
                                         + record.menu_catering_snacks_total + record.menu_catering_drinks_total \
                                         + record.menu_catering_beverages_total

    @api.model
    def create(self, vals):
        """creation of reference number and supering catering count and writing catering relation"""

        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'event.catering') or _('New')
        res = super(EventCatering, self).create(vals)
        res.event_name_id.catering_relation_id = res.id
        return res

    def button_confirm(self):
        """"change to confirmed state for booking and catering"""

        self.state = "confirmed"
        self.event_name_id.state = "confirmed"

    def button_deliver(self):
        """"change to delivered state for booking and catering"""

        self.state = "delivered"
        self.event_name_id.state = "delivered"

