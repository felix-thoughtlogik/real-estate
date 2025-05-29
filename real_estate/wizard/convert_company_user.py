from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CreateCompanyUserWizard(models.TransientModel):
    _name = 'crm.create.company.user.wizard'
    _description = 'Create Company or User Wizard'

    create_company = fields.Boolean(string="Create Company", default=True)
    create_user = fields.Boolean(string="Create User", default=True,readonly=True)

    partner_id = fields.Many2one(comodel_name='res.partner', string="Contact")
    company_id = fields.Many2one(comodel_name='res.partner', string="Company")
    email = fields.Char(string="Email", required=True)

    lead_id = fields.Many2one('crm.lead', string="Lead", required=True)

    def action_confirm(self):
        self.ensure_one()


        if self.create_company:
            self.env['res.company'].create([{
                'name': self.company_id.name,
                'partner_id':self.company_id.id,
            }])

        if self.create_user:
            if not self.email:
                raise UserError(_("Email is required to create a user."))
            user_vals = {
                'name': self.partner_id.name,
                'login': self.email,
                'partner_id': self.partner_id.id,
            }
            self.env['res.users'].create([user_vals])
