# -*- coding: utf-8 -*-

import xlsxwriter
import io
import json
from datetime import datetime

from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class EventReport(models.TransientModel):
    _name = "event.report"
    _description = "wizard report"

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    date = fields.Date(string='Current Date', default=datetime.today())
    event_type_id = fields.Many2one('event.types', string='Event Type')
    catering_ok = fields.Boolean(string='Catering orders')

    def action_done(self):
        """"generate pdf report"""

        data = self.report_query()
        return self.env.ref('event_management.action_report_event_management').report_action(self, data=data)

    def print_xlsx(self):
        """"generate xlsx report"""

        data = self.report_query()
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'event.report',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Event Management Report',
                     },
            'report_type': 'xlsx',
        }

    def report_query(self):
        """"query function"""

        event = str(self.event_type_id.id)
        to_date = str(self.to_date)
        from_date = str(self.from_date)
        query = """select b.name as bn,t.name as tn,r.name as rn,b.state,c.reference_no,b.booking_date, 
        c.menu_catering_total,c.id, cm.menu_dish_name, m.menu_dish_unit_price,m.inv_welcome_id, m.inv_breakfast_id,
        m.inv_lunch_id,m.inv_dinner_id,m.inv_snacks_id, m.inv_drinks_id,m.inv_beverages_id, m.menu_dish_subtotal,
        m.menu_dish_quantity from event_bookings as b inner join event_types as t on b.event_type_id = t.id inner 
        join res_partner as r on r.id = b.partner_id inner join event_catering as c on c.id = b.catering_relation_id 
        and c.event_name_id = b.id inner join menu_categories as m on m.inv_welcome_id = c.id or m.inv_breakfast_id = 
        c.id or m.inv_lunch_id = c.id or m.inv_dinner_id = c.id or m.inv_snacks_id = c.id or m.inv_drinks_id = c.id 
        or m.inv_beverages_id = c.id inner join event_catering_menu as cm  on cm.id = m.menu_dish_id"""

        if self.event_type_id:
            rands = self.env['event.bookings'].search([('event_type_id', '=', self.event_type_id.id)])
            if rands:
                query += " where b.event_type_id = '" + event + "'"
            else:
                raise ValidationError("event type has no bookings")
            if self.from_date:
                query += "and b.booking_date >= '" + from_date + "'"
            if self.to_date:
                query += "and b.booking_date <= '" + to_date + "'"
            if self.from_date and self.to_date and self.from_date > self.to_date:
                raise ValidationError("invalid date")
        elif self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError("invalid date")
            else:
                query += " where b.booking_date >= '" + from_date + "' and b.booking_date <= '" + to_date + "'"
        elif self.from_date:
            query += " where b.booking_date >= '" + from_date + "'"
        elif self.to_date:
            query += " where b.booking_date <= '" + to_date + "'"

        self.env.cr.execute(query)
        events = self.env.cr.dictfetchall()
        data = {
            'ids': events,
            'to_date': self.to_date,
            'from_date': self.from_date,
            'event_id': self.event_type_id.name,
            'cur_date': self.date,
            'cat_ok': self.catering_ok
        }
        return data

    def get_xlsx_report(self, data, response):
        """"xlsx display"""

        event_id = data['event_id']
        from_date = data['from_date']
        to_date = data['to_date']
        cur_date = data['cur_date']
        cat_ok = data['cat_ok']
        item = data['ids']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '15px'})
        bold = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '9px'})
        bold1 = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '8px'})
        txt1 = workbook.add_format({'font_size': '8px', 'align': 'center'})
        txt = workbook.add_format({'font_size': '9px', 'align': 'center'})
        sheet.merge_range('B2:H3', 'EVENT MANAGEMENT REPORT ', head)
        sheet.set_column(1, 1, 13)
        sheet.set_column(2, 2, 33)
        sheet.set_column(3, 6, 13)
        if event_id:
            sheet.write('B6', 'Event Type:', bold)
            sheet.write('C6', event_id, txt)
        if not from_date and not to_date:
            sheet.write('B7', 'Current Date:', bold)
            sheet.write('C7', cur_date, txt)
        if from_date:
            sheet.write('B8', 'From Date:', bold)
            sheet.write('C8', from_date, txt)
        if to_date:
            sheet.write('F8', 'To Date:', bold)
            sheet.write('G8', to_date, txt)

        sheet.write('B10', 'Sl no', bold)
        sheet.write('C10', 'event name', bold)
        if not event_id:
            sheet.write('D10', 'event type name', bold)
        sheet.write('E10', 'customer name', bold)
        sheet.write('F10', 'date', bold)
        sheet.write('G10', 'status', bold)
        sheet.write('H10', 'total', bold)
        x = 10
        y = 1
        c = 1
        lack = []
        total = 0
        for i in item:
            if not i['bn'] in lack:
                sheet.write(x, y, c, txt)
                sheet.write(x, y + 1, i['bn'], txt)
                if not event_id:
                    sheet.write(x, y + 2, i['tn'], txt)
                sheet.write(x, y + 3, i['rn'], txt)
                sheet.write(x, y + 4, i['booking_date'], txt)
                sheet.write(x, y + 5, i['state'], txt)
                sheet.write(x, y + 6, i['menu_catering_total'], txt)
                lack.append(i['bn'])
                if cat_ok:
                    row = x + 1
                    sheet.write(row, y, '')
                    sheet.write(row, y + 1, 'catering', bold1)
                    sheet.write(row, y + 2, 'item', bold1)
                    sheet.write(row, y + 3, 'quantity', bold1)
                    sheet.write(row, y + 4, 'unit price', bold1)
                    sheet.write(row, y + 5, 'sub total', bold1)
                    row1 = row + 1
                    for j in item:
                        if i['id'] == j['inv_welcome_id'] or i['id'] == j['inv_breakfast_id'] \
                                or i['id'] == j['inv_lunch_id'] or i['id'] == j['inv_dinner_id'] \
                                or i['id'] == j['inv_snacks_id'] \
                                or i['id'] == j['inv_drinks_id'] or i['id'] == j['inv_beverages_id']:
                            sheet.write(row1, y, '')
                            sheet.write(row1, y + 1, j['reference_no'], txt1)
                            sheet.write(row1, y + 2, j['menu_dish_name'], txt1)
                            sheet.write(row1, y + 3, j['menu_dish_quantity'], txt1)
                            sheet.write(row1, y + 4, j['menu_dish_unit_price'], txt1)
                            sheet.write(row1, y + 5, j['menu_dish_subtotal'], txt1)
                            row1 += 1
                            x = row1 - 1
                x += 1
                c += 1
                total += i['menu_catering_total']
        sheet.write(x + 1, y + 5, 'TOTAL AMOUNT:', bold)
        sheet.write(x + 1, y + 6, total, txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
