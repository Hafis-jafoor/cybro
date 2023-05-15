# -*- coding: utf-8 -*-

from odoo import models, api


class EventManagementReport(models.AbstractModel):
    _name = "report.event_management.report_event_management"

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_model': 'event.bookings',
            'doc_ids': docids,
            'data': data,
        }
