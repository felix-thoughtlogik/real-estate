from odoo import models,api,fields

class Lead(models.Model):
    _inherit = "crm.lead"

    requested_new_user = fields.Boolean(string='Request New User')
    new_user= fields.Many2one(comodel_name="res.partner",string="New User")

    new_user_name = fields.Char(string="Name")
    new_user_email = fields.Char(string="Email")
    new_user_phone = fields.Char(string="Phone")
    new_user_mobile = fields.Char(string="Mobile")
    new_user_job_position = fields.Char(string="Job Position")

    is_won = fields.Boolean(string="Is Won", related='stage_id.is_won')

    @api.model
    def create(self, vals):
        lead = super(Lead, self).create(vals)
        if vals.get('requested_new_user'):
            lead._create_contact()
        return lead

    def write(self, vals):
        res = super(Lead, self).write(vals)
        for record in self:
            if vals.get('requested_new_user') and record.requested_new_user:
                record._create_contact()
        return res

    def _create_contact(self):
        self.ensure_one()

        if not self.new_user_name:
            return  # Skip if name is missing

        contact_vals = {
            'name': self.new_user_name,
            'email': self.new_user_email,
            'phone': self.new_user_phone,
            'mobile': self.new_user_mobile,
            'function': self.new_user_job_position,
            'parent_id': self.partner_id.id,
            'type': 'contact',
        }

        if self.new_user:
            self.new_user.write(contact_vals)
        else:
            new_user = self.env['res.partner'].create(contact_vals)
            self.new_user = new_user.id

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
                'default_partner_id': self.new_user.id if self.new_user else self.partner_id.id,
                'default_parent_company_id': self.partner_id.id,
            },
        }
