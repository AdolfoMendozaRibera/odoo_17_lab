from odoo import models, api, fields
import pytz

class OeHealthAppointmentWhatsAppWizard(models.TransientModel):
    _inherit = "oeh.medical.appointment.whatsapp.wiz"

    @api.model
    def default_get(self, fields):
        res = super(OeHealthAppointmentWhatsAppWizard, self).default_get(fields)
        # Set default template if exists
        template = self.env.ref('module_patients_citas.whatsapp_template_appointment_reminder_2days', raise_if_not_found=False)
        if template:
            res['whatsapp_template_id'] = template.id
        return res

    @api.onchange('whatsapp_template_id')
    def onchange_whatsapp_template_id(self):
        super(OeHealthAppointmentWhatsAppWizard, self).onchange_whatsapp_template_id()
        if not self.whatsapp_template_id or not self.env.context.get('active_id'):
            return

        # Check if the selected template is our specific one, or apply logic generally?
        # Applying generally for any template using these placeholders is safer/better.
        
        appointment = self.env['oeh.medical.appointment'].browse(self.env.context.get('active_id'))
        if not appointment:
            return
        
        message = self.message or ''
        
        # Prepare values
        treatment_name = "Consulta" # Default
        if appointment.appointment_type: 
             # Get selection label
             label = dict(appointment._fields['appointment_type'].selection).get(appointment.appointment_type)
             if label:
                 treatment_name = label
             else:
                 treatment_name = appointment.appointment_type

        # Date formatting with Timezone
        if appointment.appointment_date:
            user_tz = self.env.user.tz or 'UTC'
            local_dt = pytz.utc.localize(appointment.appointment_date).astimezone(pytz.timezone(user_tz))
            date_str = local_dt.strftime('%d/%m/%Y')
            time_str = local_dt.strftime('%H:%M')
        else:
            date_str = ""
            time_str = ""

        clinic_name = appointment.institution.name if appointment.institution else "nuestra clínica"
        
        # Address construction
        address_parts = []
        if appointment.institution:
             if appointment.institution.street: address_parts.append(appointment.institution.street)
             if appointment.institution.city: address_parts.append(appointment.institution.city)
        address = ", ".join(address_parts) if address_parts else "Consultar dirección"
        
        phone = appointment.institution.mobile or appointment.institution.phone or "nosotros"

        values = {
            'treatment_name': treatment_name,
            'patient_name': appointment.patient.name or "Paciente",
            'clinic_name': clinic_name,
            'service_name': treatment_name,
            'date': date_str,
            'time': time_str,
            'doctor_name': appointment.doctor.name or "Doctor",
            'address': address,
            'phone': phone
        }

        try:
            # We use .format() but we must be careful if the message contains braces { } that are not placeholders.
            # Assuming the template follows the python format syntax provided in the request.
            formatted_message = message.format(**values)
            self.message = formatted_message
        except KeyError as e:
            # If a key is missing in values but present in template, it raises KeyError.
            # We can ignore it or try to handle it. 
            pass
        except Exception as e:
            pass
