from odoo import models, fields, api

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Department'

    name = fields.Char(string='Title', required=True)
    capacity  = fields.Char('Capacity')
    is_opened = fields.Boolean('Open')
    patients_ids = fields.One2many('hms.patient', 'department_id')
    doctor_ids = fields.One2many('hms.doctor', 'department_id')
