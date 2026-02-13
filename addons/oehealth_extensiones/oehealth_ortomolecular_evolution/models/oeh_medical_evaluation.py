from odoo import api, fields, models, _

class OeHealthPatientEvaluation(models.Model):
    _inherit = 'oeh.medical.evaluation'

    prescription_id = fields.Many2one(
        'oeh.medical.prescription', 
        string='Protocol/Prescription',
        help='Protocol or Prescription related to this evaluation'
    )

class OeHealthPrescription(models.Model):
    _inherit = 'oeh.medical.prescription'

    def action_view_evaluations(self):
        self.ensure_one()
        return {
            'name': _('Evaluations'),
            'type': 'ir.actions.act_window',
            'res_model': 'oeh.medical.evaluation',
            'view_mode': 'graph,pivot,tree,form',
            'domain': [('prescription_id', '=', self.id)],
            'context': {'default_prescription_id': self.id},
        }
