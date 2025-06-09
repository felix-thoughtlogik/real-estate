from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_seller = fields.Boolean(string="Is Seller")

class Lead(models.Model):
    _inherit = 'crm.lead'

    seller_id = fields.Many2one('res.partner',string="Seller",domain=[('is_seller', '=', True)])
    lead_type = fields.Selection([('for_seller','Related to Seller'),('for_property','Related to Property')])