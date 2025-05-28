from __future__ import annotations

from importlib.metadata import requires

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
import typing
if typing.TYPE_CHECKING:
    from odoo.addons.base.models.res_country import Country, CountryState

class PropertiesTags(models.Model):
    _name = 'real_estate.properties.tags'
    _description = 'Real Estate Property Tags'
    _rec_name = 'name'

    name = fields.Char(string='Type Name', required=True)
    description = fields.Text(string='Description')



class PropertyStage(models.Model):

    _name = "real_estate.properties.stage"
    _description = "Properties Stages"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    is_won = fields.Boolean('Is Won Stage?')
    requirements = fields.Text('Requirements', help="Enter here the internal requirements for this stage (ex: Offer sent to customer). It will appear as a tooltip over the stage's name.")

    fold = fields.Boolean('Folded in Pipeline',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')



class RealEstateProperties(models.Model):
    _name = 'real_estate.properties'
    _description = 'Real estate properties model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Property Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Property Owner', required=True)
    dealer_id = fields.Many2one('res.users', string='Dealer', default=lambda self: self.env.user)
    description = fields.Text(string='Description')

    stage_id = fields.Many2one(
        'real_estate.properties.stage', string='Stage', index=True, tracking=True,
        compute='_compute_stage_id', readonly=False, store=True,
        copy=False, group_expand='_read_group_stage_ids')
    tag_ids = fields.Many2many(
        'real_estate.properties.tags', string='Tags',
        help="Classify and analyze your Properties categories like: Training, Service")
    color = fields.Integer('Color Index', default=0)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id: CountryState = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                                             domain="[('country_id', '=?', country_id)]")
    country_id: Country = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
    price = fields.Float(string='Price', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    area_sqft = fields.Float(string='Area (sq ft)')
    bedrooms = fields.Integer(string='Bedrooms')
    bathrooms = fields.Integer(string='Bathrooms')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    swimming_pool = fields.Boolean(string='Swimming Pool')

    available_from = fields.Date(string='Available From')
    is_available = fields.Boolean(string='Is Available', default=True)
    listed_by = fields.Many2one('res.users', string='Listed By')

    image = fields.Image(string='Property Image')


    @api.model
    def _read_group_stage_ids(self, groups, domain):

        return self.env['real_estate.properties.stage'].search([])

    def _stage_find(self, limit=1):
        """ Determine the stage of the current lead with its teams, the given domain and the given team_id
            :param team_id
            :param domain : base search domain for stage
            :param order : base search order for stage
            :param limit : base search limit for stage
            :returns crm.stage recordset
        """
        return self.env['real_estate.properties.stage'].search([()], limit=limit)