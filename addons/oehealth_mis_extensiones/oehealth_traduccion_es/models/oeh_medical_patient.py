# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

class OehMedicalPatient(models.Model):
    _inherit = 'oeh.medical.patient'
    
    # Sobrescribimos el campo age con NUEVO método compute
    age = fields.Char(
        compute='_compute_age_spanish',  # NOMBRE DIFERENTE
        store=False,  # NO almacenar en BD
        size=32, 
        string='Edad del Paciente'
    )
    
    @api.depends('dob', 'deceased', 'dod')
    def _compute_age_spanish(self):
        """Calcula edad en español"""
        for patient in self:
            if not patient.dob:
                patient.age = "¡Sin fecha de nacimiento!"
                continue
            
            now = datetime.now()
            
            # Convertir dob a datetime
            if isinstance(patient.dob, str):
                dob = datetime.strptime(patient.dob, '%Y-%m-%d')
            else:
                dob = datetime.combine(patient.dob, datetime.min.time())
            
            # Si está fallecido
            if patient.deceased and patient.dod:
                if isinstance(patient.dod, str):
                    dod = datetime.strptime(patient.dod, '%Y-%m-%d')
                else:
                    dod = datetime.combine(patient.dod, datetime.min.time())
                
                delta = dod - dob
                years = delta.days // 365
                days = delta.days % 365
                patient.age = f"{years} años {days} días (fallecido)"
            else:
                delta = now - dob
                years = delta.days // 365
                days = delta.days % 365
                patient.age = f"{years} años {days} días"


class OeHealthPhysicianDegree(models.Model):
    _inherit = "oeh.medical.degrees"
    name = fields.Char(string='Degree', translate=True)
    full_name = fields.Char(string='Full Name', translate=True)

class OeHealthPhysicianSpeciality(models.Model):
    _inherit = "oeh.medical.speciality"
    name = fields.Char(string='Description', translate=True)
    code = fields.Char(string='Code', translate=True)
