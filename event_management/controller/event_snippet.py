from odoo import http
from odoo.http import request


class EventSnippet(http.Controller):
    @http.route(['/latest_events'], type="json", auth="public")
    def latest_event(self):
        """"fetching latest events """

        event_obj = request.env['event.bookings'].sudo().search_read([], ['name'], order='booking_date desc', limit=4)
        return event_obj

    @http.route('/events_website/<model("event.bookings"):event_bookings>', type="http", auth="public", website="True")
    def event_website(self, event_bookings):
        """"link events visibility on websites"""

        values = {
            'event': event_bookings,
        }
        return request.render("event_management.tmp_event_latest", values)
