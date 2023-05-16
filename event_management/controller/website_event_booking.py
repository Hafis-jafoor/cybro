from odoo import fields, http
from odoo.http import request


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

        partner_name = kw['id']
        num = partner_name.isnumeric()
        if num:
            partner = request.env['res.partner'].browse(int(partner_name))
            partner_name = partner.name
        else:
            partner = request.env['res.partner'].create({
                'name': partner_name,
                'phone': kw['phone'],
                'email': kw['email']
            })
        event_name = request.env['event.types'].browse(int(kw['event_id'])).name
        partner_id = partner.id
        first_name = partner_name.split()[0]
        if kw['event_id'] and kw['id'] and kw['event_begin_date'] and kw['event_end_date']:
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

    @http.route(['/event_relate'], type="json", auth="public")
    def event_relate(self, **kw):
        """"related fields automated"""

        var = kw['key']
        partner = request.env['res.partner'].browse(int(var))
        phone = partner.phone
        email = partner.email
        lan = {'phone': phone, 'email': email}
        return lan
