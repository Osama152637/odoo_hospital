from odoo import models, fields, api

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor'
    _rec_name = 'first_Name'

    first_Name = fields.Char(string='First Name', required=True)
    last_Name = fields.Char(string='Last Name', required=True)
    image = fields.Binary('Image')
    department_id = fields.Many2one('hms.department')
    patient_ids = fields.One2many('hms.patient', 'doctor_id')
