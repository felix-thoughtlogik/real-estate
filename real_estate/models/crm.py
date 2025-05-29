from odoo import models,api,fields

class Lead(models.Model):
    _inherit = "crm.lead"

    requested_new_user = fields.Boolean(string='Request New User')

    new_user_name = fields.Char(string="Name")  # Partner Name (Company or Person)
    new_user_email = fields.Char(string="Email")
    new_user_phone = fields.Char(string="Phone")
    new_user_mobile = fields.Char(string="Mobile")
    new_user_job_position = fields.Char(string="Job Position")
    is_won = fields.Boolean(string="Is Won", related='stage_id.is_won')

    def action_open_company_user_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.create.company.user.wizard',
            'view_mode': 'form',
            'target': 'new',
            'name': 'Create Company or User',
            'context': {
                'default_lead_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_company_id': self.partner_id.id,
                'default_email': self.email_from,
            },
        }
