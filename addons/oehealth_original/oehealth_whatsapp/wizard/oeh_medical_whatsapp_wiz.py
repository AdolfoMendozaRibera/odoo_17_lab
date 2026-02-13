# -*- coding:utf-8 -*-
##############################################################################
#    Copyright (C) 2015-Present Braincrew Apps (<http://www.braincrewapps.com>). All Rights Reserved

# Odoo Proprietary License v1.0
#
# This software and associated files (the "Software") may only be used (executed,
# modified, executed after modifications) if you have purchased a valid license
# from the authors, typically via Odoo Apps, braincrewapps.com or if you have received a written
# agreement from the authors of the Software.
#
# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the Software
# or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

##############################################################################

import datetime
import base64
from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
import urllib
import re
from odoo.http import request
import json
import requests
import logging

_logger = logging.getLogger(__name__)
from odoo.tools.mimetypes import guess_mimetype


class oeHealthWhatsAppWizard(models.TransientModel):
    _name = "oeh.medical.whatsapp.wiz"
    _description = "WhatsApp Wizard"

    name = fields.Many2one('oeh.medical.patient', string='Patient', domain="[('id','=',name)]")
    whatsapp_template_id = fields.Many2one('oeh.medical.whatsapp.template', string='Template')
    mobile = fields.Char(related='name.mobile')
    message = fields.Text(string="Message")
    staff_ids = fields.Many2many('oeh.medical.physician', string='Staff', domain="[('mobile_phone', '!=', False)]")
    attachment_ids = fields.Many2many('ir.attachment', string='Send multiple files')

    @api.onchange('whatsapp_template_id')
    def onchange_whatsapp_template_id(self):
        formatted_message = ''
        if self.name and self.whatsapp_template_id and self.whatsapp_template_id.message:
            formatted_message = self.whatsapp_template_id.message
            self.message = formatted_message

    def send_message_through_chat_api(self, number, message):
        # messege_to_send_encoded = messege_to_send.encode('utf-8')
        instance_id = self.env.company.chat_api_instance_id
        instance_token = self.env.company.chat_api_instance_token
        data = {'phone': number, 'body': str(message)}
        full_url = _('https://api.chat-api.com/instance%s/sendMessage?token=%s') % (
            str(instance_id), str(instance_token))
        headers = {
            'Content-type': 'application/json',
        }
        req = requests.post(full_url, data=json.dumps(data), headers=headers)
        req.raise_for_status()
        content = req.json()
        if content.get('sent'):
            _logger.info('WhatsApp message successfully sent to %s', number)
        if self.attachment_ids:
            for f in self.attachment_ids:
                file_content = _('data:%s;base64,%s') % (str(f.mimetype), str(f.datas.decode('utf-8')))
                file_message_data = {'phone': number, 'body': file_content, 'filename': f.name}
                file_full_url = _('https://api.chat-api.com/instance%s/sendFile?token=%s') % (
                    str(instance_id), str(instance_token))
                file_req = requests.post(file_full_url, data=json.dumps(file_message_data), headers=headers)
                file_req.raise_for_status()
                file_response = file_req.json()
                if file_response.get('sent'):
                    _logger.info('File successfully sent to %s', number)

    def send_whatsapp_msg(self):
        record = self._context.get('active_ids', [])
        if not self.name:
            raise ValidationError(_("Patient not found !"))
        if not self.mobile:
            raise ValidationError(_("Mobile number not found !"))

        whatsapp_number = self.mobile
        formatted_message = u'{}'.format(self.message)
        if self.name:
            messege_to_send = self.name.name
        else:
            messege_to_send = ''

        if self.whatsapp_template_id:
            messege_to_send += '\r\n' + str(self.whatsapp_template_id.name)

        messege_to_send += '\r\n' + formatted_message

        if self.env.company.enable_chat_api:
            self.send_message_through_chat_api(number=whatsapp_number, message=messege_to_send)
            return True
        else:
            messege_to_send_encoded = urllib.parse.quote(messege_to_send.encode('utf-8'))
            mobileRegex = r"android|webos|iphone|ipod|blackberry|iemobile|opera mini"
            user_agent = request.httprequest.environ.get('HTTP_USER_AGENT', '').lower()
            match = re.search(mobileRegex, user_agent)

            if match:
                whatsapp_url = 'https://api.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number,
                                                                                       messege_to_send_encoded)
            else:
                whatsapp_url = 'https://web.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number,
                                                                                       messege_to_send_encoded)

            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'name': "whatsapp_action",
                'target': 'new',
            }


class oeHealthMedicalStaffWhatsAppWizard(models.TransientModel):
    _name = "oeh.medical.staff.whatsapp.wiz"
    _description = "Medical Staff WhatsApp Wizard"

    name = fields.Many2one('oeh.medical.physician', string='Staff', domain="[('id','=',name)]")
    whatsapp_template_id = fields.Many2one('oeh.medical.whatsapp.template', string='Template')
    mobile = fields.Char(related='name.mobile_phone')
    message = fields.Text(string="Message")
    attachment_ids = fields.Many2many('ir.attachment', string='Send multiple files')

    @api.onchange('whatsapp_template_id')
    def onchange_whatsapp_template_id(self):
        formatted_message = ''
        # active_model = self.env.context.get('active_model')
        # record = self.env[active_model].browse(self.env.context.get('active_id')).exists()
        if self.name and self.whatsapp_template_id and self.whatsapp_template_id.message:
            formatted_message = self.whatsapp_template_id.message
        self.message = formatted_message

    def send_message_through_chat_api(self, number, message):
        # messege_to_send_encoded = messege_to_send.encode('utf-8')
        instance_id = self.env.company.chat_api_instance_id
        instance_token = self.env.company.chat_api_instance_token
        data = {'phone': number, 'body': str(message)}
        full_url = _('https://api.chat-api.com/instance%s/sendMessage?token=%s') % (
            str(instance_id), str(instance_token))
        headers = {
            'Content-type': 'application/json',
        }
        req = requests.post(full_url, data=json.dumps(data), headers=headers)
        req.raise_for_status()
        content = req.json()
        if content.get('sent'):
            _logger.info('WhatsApp message successfully sent to %s', number)
        if self.attachment_ids:
            for f in self.attachment_ids:
                file_content = _('data:%s;base64,%s') % (str(f.mimetype), str(f.datas.decode('utf-8')))
                file_message_data = {'phone': number, 'body': file_content, 'filename': f.name}
                file_full_url = _('https://api.chat-api.com/instance%s/sendFile?token=%s') % (
                    str(instance_id), str(instance_token))
                file_req = requests.post(file_full_url, data=json.dumps(file_message_data), headers=headers)
                file_req.raise_for_status()
                file_response = file_req.json()
                if file_response.get('sent'):
                    _logger.info('File successfully sent to %s', number)

    def send_whatsapp_msg(self):
        record = self._context.get('active_ids', [])
        if not self.name:
            raise ValidationError(_("Medical staff not selected !"))
        if not self.name.mobile_phone:
            raise ValidationError(_("Mobile number not found !"))

        whatsapp_number = self.name.mobile_phone
        messege_to_send = u'{}'.format(self.message)
        messege_to_send = messege_to_send


        if self.env.company.enable_chat_api:
            self.send_message_through_chat_api(number=whatsapp_number, message=messege_to_send)
            return True
        else:
            messege_to_send_encoded = urllib.parse.quote(messege_to_send.encode('utf-8'))
            mobileRegex = r"android|webos|iphone|ipod|blackberry|iemobile|opera mini"
            user_agent = request.httprequest.environ.get('HTTP_USER_AGENT', '').lower()
            match = re.search(mobileRegex, user_agent)

            if match:
                whatsapp_url = 'https://api.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number,
                                                                                       messege_to_send_encoded)
            else:
                whatsapp_url = 'https://web.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number,
                                                                                       messege_to_send_encoded)

            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'name': "whatsapp_action",
                'target': 'new',
            }


class oeHealthAppointmentWhatsAppWizard(models.TransientModel):
    _name = "oeh.medical.appointment.whatsapp.wiz"
    _description = "Appointment WhatsApp Wizard"

    name = fields.Many2one('oeh.medical.patient', string='Patient', domain="[('id','=',name)]")
    doctor = fields.Many2one('oeh.medical.physician', string='Staff', domain="[('id','=',name)]")
    whatsapp_template_id = fields.Many2one('oeh.medical.whatsapp.template', string='Template')
    message = fields.Text(string="Message")
    attachment_ids = fields.Many2many('ir.attachment', string='Send multiple files')

    @api.onchange('whatsapp_template_id')
    def onchange_whatsapp_template_id(self):
        formatted_message = ''
        # active_model = self.env.context.get('active_model')
        # record = self.env[active_model].browse(self.env.context.get('active_id')).exists()
        if self.name and self.whatsapp_template_id and self.whatsapp_template_id.message:
            formatted_message = self.whatsapp_template_id.message
        self.message = formatted_message

    def send_message_through_chat_api(self, number, message):
        # messege_to_send_encoded = messege_to_send.encode('utf-8')
        instance_id = self.env.company.chat_api_instance_id
        instance_token = self.env.company.chat_api_instance_token
        data = {'phone': number, 'body': str(message)}
        full_url = _('https://api.chat-api.com/instance%s/sendMessage?token=%s') % (
            str(instance_id), str(instance_token))
        headers = {
            'Content-type': 'application/json',
        }
        req = requests.post(full_url, data=json.dumps(data), headers=headers)
        req.raise_for_status()
        content = req.json()
        if content.get('sent'):
            _logger.info('WhatsApp message successfully sent to %s', number)
        if self.attachment_ids:
            for f in self.attachment_ids:
                file_content = _('data:%s;base64,%s') % (str(f.mimetype), str(f.datas.decode('utf-8')))
                file_message_data = {'phone': number, 'body': file_content, 'filename': f.name}
                file_full_url = _('https://api.chat-api.com/instance%s/sendFile?token=%s') % (
                    str(instance_id), str(instance_token))
                file_req = requests.post(file_full_url, data=json.dumps(file_message_data), headers=headers)
                file_req.raise_for_status()
                file_response = file_req.json()
                if file_response.get('sent'):
                    _logger.info('File successfully sent to %s', number)

    def send_whatsapp_msg(self):
        record = self._context.get('active_ids', [])
        if not self.name:
            raise ValidationError(_("Medical staff not selected !"))
        if not self.name.mobile:
            raise ValidationError(_("Patient Mobile number not found !"))
        if not self.doctor.mobile_phone:
            raise ValidationError(_("Doctor Mobile number not found !"))

        whatsapp_number = self.name.mobile
        formatted_message = u'{}'.format(self.message)
        if self.name:
            messege_to_send = self.name.name
        else:
            messege_to_send = ''

        if self.whatsapp_template_id:
            messege_to_send += '\r\n' + str(self.whatsapp_template_id.name)

        messege_to_send += '\r\n' + formatted_message

        if self.env.company.enable_chat_api:
            self.send_message_through_chat_api(number=whatsapp_number, message=messege_to_send)
            return True
        else:
            messege_to_send_encoded = urllib.parse.quote(messege_to_send.encode('utf-8'))
            mobileRegex = r"android|webos|iphone|ipod|blackberry|iemobile|opera mini"
            user_agent = request.httprequest.environ.get('HTTP_USER_AGENT', '').lower()
            match = re.search(mobileRegex, user_agent)

            if match:
                whatsapp_url = 'https://api.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number,
                                                                                       messege_to_send_encoded)
            else:
                whatsapp_url = 'https://web.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number,
                                                                                       messege_to_send_encoded)

            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'name': "whatsapp_action",
                'target': 'new',
            }


class oeHealthLabTestWhatsAppWizard(models.TransientModel):
    _name = "oeh.medical.lab.test.whatsapp.wiz"
    _description = "Lab Test WhatsApp Wizard"

    name = fields.Many2one('oeh.medical.patient', string='Patient', domain="[('id','=',name)]")
    whatsapp_template_id = fields.Many2one('oeh.medical.whatsapp.template', string='Template')
    message = fields.Text(string="Message")
    # res_id = fields.Integer('Document ID', required=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Send multiple files')


    @api.onchange('whatsapp_template_id')
    def onchange_whatsapp_template_id(self):
        formatted_message = ''
        # active_model = self.env.context.get('active_model')
        # record = self.env[active_model].browse(self.env.context.get('active_id')).exists()
        if self.name and self.whatsapp_template_id and self.whatsapp_template_id.message:
            formatted_message = self.whatsapp_template_id.message
        self.message = formatted_message

    def send_message_through_chat_api(self, number, message):
        # messege_to_send_encoded = messege_to_send.encode('utf-8')
        instance_id = self.env.company.chat_api_instance_id
        instance_token = self.env.company.chat_api_instance_token
        data = {'phone': number, 'body': str(message)}
        full_url = _('https://api.chat-api.com/instance%s/sendMessage?token=%s') % (
            str(instance_id), str(instance_token))
        headers = {
            'Content-type': 'application/json',
        }
        req = requests.post(full_url, data=json.dumps(data), headers=headers)
        req.raise_for_status()
        content = req.json()
        if content.get('sent'):
            _logger.info('WhatsApp message successfully sent to %s', number)
        if self.attachment_ids:
            for f in self.attachment_ids:
                file_content = _('data:%s;base64,%s') % (str(f.mimetype), str(f.datas.decode('utf-8')))
                file_message_data = {'phone': number, 'body': file_content, 'filename': f.name}
                file_full_url = _('https://api.chat-api.com/instance%s/sendFile?token=%s') % (
                    str(instance_id), str(instance_token))
                file_req = requests.post(file_full_url, data=json.dumps(file_message_data), headers=headers)
                file_req.raise_for_status()
                file_response = file_req.json()
                if file_response.get('sent'):
                    _logger.info('File successfully sent to %s', number)



    @api.model
    def default_get(self, fields):
        res = super(oeHealthLabTestWhatsAppWizard, self).default_get(fields)

        # lab_test_id = self.env['oeh.medical.lab.test'].browse(self.env.context['active_ids'])
        #
        # pdf = self.env.ref('oehealth_lab.action_report_patient_labtest')._render_qweb_pdf(lab_test_id.id)
        # b64_pdf = base64.b64encode(pdf[0])
        #
        # attachment = self.env['ir.attachment'].create({
        #     'name': "Lab Test Report.pdf",
        #     'datas': b64_pdf,
        #     'public':True,
        #     'res_model': 'oeh.medical.lab.test.whatsapp.wiz',
        #     'res_id': self.id,
        #     'type': 'binary',  # override default_type from context, possibly meant for another model!
        # })
        # res.update({
        #     'attachment_ids': attachment.ids
        # })
        return res


    def send_whatsapp_msg(self):
        record = self._context.get('active_ids', [])

        if not self.name:
            raise ValidationError(_("Medical staff not selected !"))
        if not self.name.mobile:
            raise ValidationError(_("Patient Mobile number not found !"))

        whatsapp_number = self.name.mobile
        formatted_message = u'{}'.format(self.message)
        if self.name:
            messege_to_send = self.name.name
        else:
            messege_to_send = ''

        if self.whatsapp_template_id:
            messege_to_send += '\r\n' + str(self.whatsapp_template_id.name)

        messege_to_send += '\r\n' + formatted_message

        if self.env.company.enable_chat_api:
            self.send_message_through_chat_api(number=whatsapp_number, message=messege_to_send)
            return True
        else:
            messege_to_send_encoded = urllib.parse.quote(messege_to_send.encode('utf-8'))
            mobileRegex = r"android|webos|iphone|ipod|blackberry|iemobile|opera mini"
            user_agent = request.httprequest.environ.get('HTTP_USER_AGENT', '').lower()
            match = re.search(mobileRegex, user_agent)

        if match:
            whatsapp_url = 'https://api.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number,
                                                                                   messege_to_send_encoded)
        else:
            whatsapp_url = 'https://web.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number,
                                                                                   messege_to_send_encoded)

        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'name': "whatsapp_action",
            'target': 'new',
        }


class oeHealthPrescriptionWhatsAppWizard(models.TransientModel):
    _name = "oeh.medical.prescription.whatsapp.wiz"
    _description = "Prescription WhatsApp Wizard"

    name = fields.Many2one('oeh.medical.patient', string='Patient', domain="[('id','=',name)]")
    whatsapp_template_id = fields.Many2one('oeh.medical.whatsapp.template', string='Template')
    message = fields.Text(string="Message")
    attachment_ids = fields.Many2many('ir.attachment', string='Send multiple files')

    @api.onchange('whatsapp_template_id')
    def onchange_whatsapp_template_id(self):
        formatted_message = ''
        # active_model = self.env.context.get('active_model')
        # record = self.env[active_model].browse(self.env.context.get('active_id')).exists()
        if self.name and self.whatsapp_template_id and self.whatsapp_template_id.message:
            formatted_message = self.whatsapp_template_id.message
        self.message = formatted_message

    def send_message_through_chat_api(self, number, message):
        # messege_to_send_encoded = messege_to_send.encode('utf-8')
        instance_id = self.env.company.chat_api_instance_id
        instance_token = self.env.company.chat_api_instance_token
        data = {'phone': number, 'body': str(message)}
        full_url = _('https://api.chat-api.com/instance%s/sendMessage?token=%s') % (
            str(instance_id), str(instance_token))
        headers = {
            'Content-type': 'application/json',
        }
        req = requests.post(full_url, data=json.dumps(data), headers=headers)
        req.raise_for_status()
        content = req.json()
        if content.get('sent'):
            _logger.info('WhatsApp message successfully sent to %s', number)
        if self.attachment_ids:
            for f in self.attachment_ids:
                file_content = _('data:%s;base64,%s') % (str(f.mimetype), str(f.datas.decode('utf-8')))
                file_message_data = {'phone': number, 'body': file_content, 'filename': f.name}
                file_full_url = _('https://api.chat-api.com/instance%s/sendFile?token=%s') % (
                    str(instance_id), str(instance_token))
                file_req = requests.post(file_full_url, data=json.dumps(file_message_data), headers=headers)
                file_req.raise_for_status()
                file_response = file_req.json()
                if file_response.get('sent'):
                    _logger.info('File successfully sent to %s', number)


    @api.model
    def default_get(self, fields):
        res = super(oeHealthPrescriptionWhatsAppWizard, self).default_get(fields)

        # prescription_id = self.env['oeh.medical.prescription'].browse(self.env.context['active_ids'])
        #
        # pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf(
        #     'oehealth.action_oeh_medical_report_patient_prescriptions',
        #     prescription_id.ids,
        # )[0]
        #
        # b64_pdf = base64.encodestring(pdf)
        # file_data_to_send = b64_pdf.decode('utf-8')
        #
        # attachment = self.env['ir.attachment'].create({
        #     'name': "Prescription Report.pdf",
        #     'datas': file_data_to_send,
        #     'public': True,
        #     'res_model': 'oeh.medical.prescription.whatsapp.wiz',
        #     'res_id': self.id,
        #     'type': 'binary',  # override default_type from context, possibly meant for another model!
        # })
        # res.update({
        #     'attachment_ids': attachment.ids
        # })
        return res

    def send_whatsapp_msg(self):
        record = self._context.get('active_ids', [])
        if not self.name:
            raise ValidationError(_("Medical staff not selected !"))
        if not self.name.mobile:
            raise ValidationError(_("Patient Mobile number not found !"))

        whatsapp_number = self.name.mobile
        formatted_message = u'{}'.format(self.message)
        if self.name:
            messege_to_send = self.name.name
        else:
            messege_to_send = ''

        if self.whatsapp_template_id:
            messege_to_send += '\r\n' + str(self.whatsapp_template_id.name)

        messege_to_send += '\r\n' + formatted_message

        if self.env.company.enable_chat_api:
            self.send_message_through_chat_api(number=whatsapp_number, message=messege_to_send)
            return True
        else:
            messege_to_send_encoded = urllib.parse.quote(messege_to_send.encode('utf-8'))
            mobileRegex = r"android|webos|iphone|ipod|blackberry|iemobile|opera mini"
            user_agent = request.httprequest.environ.get('HTTP_USER_AGENT', '').lower()
            match = re.search(mobileRegex, user_agent)

            if match:
                whatsapp_url = 'https://api.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number,
                                                                                       messege_to_send_encoded)
            else:
                whatsapp_url = 'https://web.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number,
                                                                                       messege_to_send_encoded)

            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'name': "whatsapp_action",
                'target': 'new',
            }
