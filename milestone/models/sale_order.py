# -*- coding: utf-8 -*-


from odoo import models, fields, api


class SaleOrder(models.Model):
    """"sale order  management"""

    _inherit = 'sale.order'

    project_ok = fields.Boolean(string='project')
    project_id = fields.Many2one('project.project', string='project')

    def create_project(self):
        """"create project of this order"""

        project_view = {
            'name': self.name,
            'partner_id': self.partner_id.id,

        }
        vals = self.env['project.project'].create(project_view)
        self.write({'project_ok': True, 'project_id': vals.id})
        self.project_create()

        return {
            'type': 'ir.actions.act_window',
            'name': 'project',
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': self.project_id.id,
        }

    def update_project(self):
        """"update the project of order"""
        #
        for j in self.project_id.tasks:
            j.unlink()
        self.project_create()

    def project_create(self):
        """"create project function"""

        milestone_count = {}
        for record in self.order_line:
            if record.milestone_no in milestone_count:
                milestone_count[record.milestone_no] += [record.product_id]
            else:
                milestone_count[record.milestone_no] = [record.product_id]

        for record in milestone_count:
            task_name = "milestone" + "" + str(record)
            subtask = []
            val = len(milestone_count[record])
            if val > 1:
                subtask = [fields.Command.create({'name': task_name + "-" + task_name + "-" + str(i.name)})
                           for i in milestone_count[record]]
            task_view = {
                'name': task_name,
                'child_ids': subtask,
                'project_id': self.project_id.id,
            }
            self.project_id.tasks.create(task_view)

    def get_project(self):
        """"project page redirect"""

        return {
            'type': 'ir.actions.act_window',
            'name': 'project ',
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': self.project_id.id,
        }
