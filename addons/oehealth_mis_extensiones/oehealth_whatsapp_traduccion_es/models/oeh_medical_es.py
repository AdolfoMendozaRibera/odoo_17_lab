from odoo import models, api, _

class OeHealthPatient(models.Model):
    _inherit = 'oeh.medical.patient'

    def send_whatsapp_to_patient(self):
        res = super(OeHealthPatient, self).send_whatsapp_to_patient()
        if isinstance(res, dict):
            res['name'] = "Enviar WhatsApp"
        return res

class OeHealthMedicalPhysician(models.Model):
    _inherit = 'oeh.medical.physician'

    def send_whatsapp_to_medical_staff(self):
        res = super(OeHealthMedicalPhysician, self).send_whatsapp_to_medical_staff()
        if isinstance(res, dict):
            res['name'] = "Enviar WhatsApp"
        return res

class OeHealthMedicalAppointment(models.Model):
    _inherit = 'oeh.medical.appointment'

    def send_appointment_detail_whatsapp_(self):
        res = super(OeHealthMedicalAppointment, self).send_appointment_detail_whatsapp_()
        if isinstance(res, dict):
            res['name'] = "Enviar WhatsApp"
        return res

class OeHealthMedicalLabtest(models.Model):
    _inherit = 'oeh.medical.lab.test'

    def send_lab_test_detail_whatsapp_(self):
        res = super(OeHealthMedicalLabtest, self).send_lab_test_detail_whatsapp_()
        if isinstance(res, dict):
            res['name'] = "Enviar WhatsApp"
        return res

class OeHealthMedicalPrescription(models.Model):
    _inherit = 'oeh.medical.prescription'

    def send_prescription_detail_whatsapp_(self):
        res = super(OeHealthMedicalPrescription, self).send_prescription_detail_whatsapp_()
        if isinstance(res, dict):
            res['name'] = "Enviar WhatsApp"
        return res
