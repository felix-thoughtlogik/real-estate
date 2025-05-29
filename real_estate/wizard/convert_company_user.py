from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CreateCompanyUserWizard(models.TransientModel):
    _name = 'crm.create.company.user.wizard'
    _description = 'Create Company or User Wizard'

    create_company = fields.Boolean(string="Create Company", compute="_compute_create_company")
    create_user = fields.Boolean(string="Create User", default=True,readonly=True)
    company_exists = fields.Boolean(string="Company Exists")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Contact")
    partner_name = fields.Char(string="User Name",related="partner_id.name")
    partner_email = fields.Char(string="User Email",related="partner_id.email")
    parent_company_id = fields.Many2one(comodel_name='res.partner', string="Company")
    parent_company_name = fields.Char(string="Company Name", related="parent_company_id.name")
    parent_company_email = fields.Char(string="User Email", related="parent_company_id.email")

    lead_id = fields.Many2one('crm.lead', string="Lead", required=True)

    @api.depends('parent_company_id')
    def _compute_create_company(self):
        for wizard in self:
            company = self.env['res.company'].search([
                ('partner_id', '=', wizard.parent_company_id.id)
            ], limit=1)

            if company:
                wizard.create_company = False
                wizard.company_exists = True
            else:
                wizard.create_company = True
                wizard.company_exists = False

    def action_confirm(self):
        self.ensure_one()

        new_company = None
        if self.create_company:
            new_company = self.env['res.company'].create({
                'name': self.parent_company_id.name,
                'partner_id': self.parent_company_id.id,
            })

        if self.create_user:
            if not self.partner_id.email:
                raise UserError(_("Cannot create user without an email (login)."))

            if new_company:
                company_id = new_company.id
            else:
                existing_company = self.env['res.company'].search([
                    ('partner_id', '=', self.parent_company_id.id)
                ], limit=1)
                if not existing_company:
                    raise UserError(_("No company found linked to this partner."))
                company_id = existing_company.id

            user_vals = {
                'name': self.partner_id.name,
                'login': self.partner_id.email,
                'partner_id': self.partner_id.id,
                'company_id': company_id,
                'company_ids': [(6, 0, [company_id])],
            }

            self.env['res.users'].create(user_vals)

        return True

