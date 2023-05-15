from odoo import http, fields
from odoo.http import request
from datetime import datetime


class WebsiteEventBooking(http.Controller):
    @http.route('/event', type='http', auth="user", website=True)
    def booking(self):
        """"datas passing to event booking template"""
        date = fields.date.today()
        partners = request.env['res.partner'].sudo().search([])
        types = request.env['event.types'].sudo().search([])
        values = {}
        values.update({
            'partners': partners,
            'types': types,
            'date': date,
        })
        return request.render("event_management.online_event_booking", values)

    @http.route('/event/submit/', type='http', methods=['POST'], auth="public", website=True, csrf=False)
    def event_booking_form(self, **kw):
        """"creation of bookings from website"""

        partner_name = kw['name']
        partner = request.env['res.partner'].search([('name', '=', partner_name)])
        print('sa', partner)
        if not partner:
            partner = request.env['res.partner'].create({
                'name': partner_name,
                'phone': kw['phone'],
                'email': kw['email']
            })
        event_name = request.env['event.types'].browse(int(kw['event_id'])).name
        partner_id = partner.id
        first_name = partner_name.split()[0]
        if kw['event_id'] and kw['name'] and kw['event_begin_date'] and kw['event_end_date']:
            value = f"{event_name} : {first_name} / {kw['event_begin_date']} : {kw['event_end_date']}"
        create_booking = {
            'name': value,
            'event_type_id': kw['event_id'],
            'partner_id': partner_id,
            'booking_date': kw['event_booking_date'],
            'begin_date': kw['event_begin_date'],
            'end_date': kw['event_end_date'],
        }
        request.env['event.bookings'].create(create_booking)

        return request.render("event_management.website_event_confirmed")

