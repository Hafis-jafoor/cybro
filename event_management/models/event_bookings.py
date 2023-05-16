# -*- coding: utf-8 -*-


from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError


class EventBookings(models.Model):
    """event booking Management"""

    _name = "event.bookings"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "event bookings"

    name = fields.Char(compute='_compute_name', readonly="true", default="new", store=True)
    event_type_id = fields.Many2one('event.types', string='Event Type', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    booking_date = fields.Date(string='Booking Date', default=fields.Datetime.now)
    begin_date = fields.Datetime(string='Event Begin Date', required=True)
    end_date = fields.Datetime(string='Event End Date', required=True)
    duration = fields.Integer(compute='_onchange_calculate_date', string="Duration", readonly="true")
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('delivered', 'Delivered'),
                              ('invoiced', 'Invoiced'),
                              ('expired', 'Expired'), ],
                             string='status', default='draft')
    catering_count = fields.Integer(compute='_compute_count')
    invoice_id = fields.Many2one('account.move', string='Payment Reference', readonly=True, store=True)
    payment_state = fields.Selection(related='invoice_id.payment_state')
    catering_relation_id = fields.Many2one('event.catering', readonly=True, string='Catering Reference')
    catering_state = fields.Selection(related='catering_relation_id.state')

    # purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')

    @api.onchange('begin_date', 'end_date')
    def _onchange_calculate_date(self):
        """duration calculation"""

        for record in self:
            if record.begin_date and record.end_date and record.begin_date > record.end_date:
                raise ValidationError("INVALID DATE")
            elif record.begin_date and record.end_date:
                difference = record.end_date - record.begin_date
                record.duration = difference.days + 1

    @api.depends('event_type_id', 'partner_id', 'begin_date', 'end_date')
    def _compute_name(self):
        """"concatenation of fields to main name"""

        print(self.begin_date)
        for record in self:
            if record.event_type_id.name and record.partner_id.name and record.begin_date and record.end_date:
                begin_date_only = record.begin_date.strftime("%Y-%m-%d")
                end_date_only = record.end_date.strftime("%Y-%m-%d")
                first_name = record.partner_id.name.split()[0]
                record.name = f"{record.event_type_id.name} : {first_name} / {begin_date_only} : {end_date_only}"

    def action_date(self):
        """"state change to expiry after begin"""

        for record in self.search([('state', '=', 'draft')]):
            if record.begin_date:
                if datetime.today() > record.begin_date:
                    record.state = "expired"
                else:
                    record.state = "draft"

    @api.onchange('begin_date', 'state')
    def action_non_date(self):
        """"state change to the expiry after begin"""

        for record in self:
            if record.begin_date:
                if datetime.today() > record.begin_date:
                    record.state = "expired"
                else:
                    record.state = "draft"

    def button_catering_service(self):
        """"catering creation for booking"""

        return {
            'type': 'ir.actions.act_window',
            'name': 'catering service',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'event.catering',
            'context': {'default_event_name_id': self.id}
        }

    def button_confirm(self):
        """"change to confirmed state for both catering and booking"""

        self.state = "confirmed"
        self.catering_relation_id.state = "confirmed"
        # self.purchase_order_id.button_confirm()

    def button_deliver(self):
        """"change to delivered state for booking and catering"""

        self.state = "delivered"
        self.catering_relation_id.state = "delivered"

    def get_catering(self):
        """"smart button redirecting to catering page"""

        return {
            'type': 'ir.actions.act_window',
            'name': 'event catering',
            'view_mode': 'form',
            'res_model': 'event.catering',
            'res_id': self.catering_relation_id.id

        }

    def _compute_count(self):
        """"calculation of caterings of event booking"""

        for record in self:
            record.catering_count = self.catering_relation_id.search_count(
                [('event_name_id', '=', self.id)])

    def button_invoice(self):
        """"invoice generation"""

        order_lines = []
        for record in self:
            lines = record.catering_relation_id.welcome_drink_ids + record.catering_relation_id.break_fast_ids \
                    + record.catering_relation_id.snacks_ids + record.catering_relation_id.drinks_ids \
                    + record.catering_relation_id.beverages_ids \
                    + record.catering_relation_id.dinner_ids + record.catering_relation_id.lunch_ids
            for i in lines:
                order_lines.append(fields.Command.create({
                    'name': i.menu_dish_id.menu_dish_name,
                    'quantity': i.menu_dish_quantity,
                    'price_unit': i.menu_dish_unit_price,
                    'price_subtotal': i.menu_dish_subtotal,
                }))
        delivery_invoice = {
            'move_type': 'out_invoice',
            'invoice_origin': record.catering_relation_id.reference_no,
            'invoice_date': fields.Date.context_today(record),
            'partner_id': record.partner_id.id,
            'currency_id': record.catering_relation_id.currency_id.id,
            'amount_total': record.catering_relation_id.menu_catering_total,
            'invoice_line_ids': order_lines,
        }
        invoice_vals = self.env['account.move'].create(delivery_invoice)
        self.write({'state': 'invoiced', 'invoice_id': invoice_vals.id})
        return {
            'type': 'ir.actions.act_window',
            'name': 'invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice_vals.id,
        }

    def get_payment(self):
        """"smart button redirecting to payment page"""

        return {
            'type': 'ir.actions.act_window',
            'name': 'invoice ',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
        }
