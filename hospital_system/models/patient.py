from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import re


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = 'first_Name'

    first_Name = fields.Char(string='First Name', required=True)
    last_Name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date('Birth date')
    history = fields.Html('History')
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')
    ])
    pcr = fields.Boolean('PCR')
    image = fields.Binary('Image')
    address = fields.Text('Address')
    age = fields.Integer(compute='_compute_age')
    states = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')
    department_id = fields.Many2one('hms.department')
    doctor_id = fields.Many2one('hms.doctor')
    log_history = fields.One2many('hms.log.history', 'patient_id')
    email = fields.Char()

    def action_undetermined(self):
        self.write({'states': 'undetermined'})
        self.env['hms.log.history'].create({
            'patient_id': self.id,
            'description': 'The State Changed To Undetermined'
        })

    def action_good(self):
        self.write({'states': 'good'})
        self.env['hms.log.history'].create({
            'patient_id': self.id,
            'description': 'The State Changed To Good'
        })

    def action_fair(self):
        self.write({'states': 'fair'})
        self.env['hms.log.history'].create({
            'patient_id': self.id,
            'description': 'The State Changed To Fair'
        })

    def action_serious(self):
        self.write({'states': 'serious'})
        self.env['hms.log.history'].create({
            'patient_id': self.id,
            'description': 'The State Changed To Serious'
        })

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = relativedelta(fields.Date.today(), rec.birth_date).years
            else:
                rec.age = 0

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR ratio must be provided when PCR is checked.")

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            if not self.pcr:
                self.pcr = True
                return {
                    'warning': {
                        'title': 'PCR Field Checked',
                        'message': 'The PCR field has been automatically checked because the age is below 30.',
                    }
                }
        else:
            self.pcr = False

    def action_open_add_log_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hms.add.new.log',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_patient_id': self.id},
        }

    @api.constrains('email')
    def _check_email_validity(self):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        for rec in self:
            if rec.email and not re.match(email_regex, rec.email):
                raise ValidationError('Please enter a valid email address.')

    _sql_constraints = [
        ('unique_email', 'unique(email)', 'The email address must be unique.')
    ]


class LogHistory(models.Model):
    _name = 'hms.log.history'
    _description = 'Log History'

    patient_id = fields.Many2one('hms.patient')
    description = fields.Text()
    date = fields.Datetime(default=fields.Datetime.now)
