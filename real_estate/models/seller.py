from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_seller = fields.Boolean(string="Is Seller")


class Lead(models.Model):
    _inherit = 'crm.lead'

    seller_id = fields.Many2one('res.partner', string="Seller", domain=[('is_seller', '=', True)])
    lead_type = fields.Selection([('for_seller','Related to Seller'),('for_property','Related to Property')])

    is_won = fields.Boolean(string="Is Won", related='stage_id.is_won', store=True)

    def action_open_seller(self):
        self.ensure_one()

        if not self.partner_id:
            raise UserError("No customer/contact (partner) is linked to this lead.")

        # Update is_seller and address fields
        self.partner_id.write({
            'is_seller': True,
            'street': self.street or '',
            'street2': self.street2 or '',
            'city': self.city or '',
            'state_id': self.state_id.id if self.state_id else False,
            'zip': self.zip or '',
            'country_id': self.country_id.id if self.country_id else False,
            'phone': self.phone or '',
            'mobile': self.mobile or '',
            'email': self.email_from or '',
            'website':self.website or '',
        })

        return {
            'name': 'Seller Details',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'view_mode': 'form',
            'target': 'new',
        }

