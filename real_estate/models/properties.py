from __future__ import annotations

from importlib.metadata import requires

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
import typing
if typing.TYPE_CHECKING:
    from odoo.addons.base.models.res_country import Country, CountryState

class PropertiesTags(models.Model):
    _name = 'property.tag'
    _description = 'Real Estate Property Tags'
    _rec_name = 'name'

    name = fields.Char(string='Type Name', required=True)
    description = fields.Text(string='Description')



class PropertyStage(models.Model):

    _name = "property.stage"
    _description = "Properties Stages"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    is_won = fields.Boolean('Is Won Stage?')
    requirements = fields.Text('Requirements', help="Enter here the internal requirements for this stage (ex: Offer sent to customer). It will appear as a tooltip over the stage's name.")

    fold = fields.Boolean('Folded in Pipeline',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')


class PropertyImage(models.Model):
    _name = 'property.image'
    _description = 'Additional Images for Properties'

    name = fields.Char(string='Description')
    image = fields.Image(string='Image')
    property_id = fields.Many2one('property.property', string='Property', required=True, ondelete='cascade')

class PropertyAmenity(models.Model):
    _name = 'property.amenity'
    _description = 'Property Amenity'

    name = fields.Char(string="Amenity Name", required=True)
    icon = fields.Char(string="Icon")
    description = fields.Text(string='Description')

class PropertyFloorType(models.Model):
    _name = 'property.floor.type'
    _description = 'Property Floor Type'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string='Description')




class RealEstateProperties(models.Model):
    _name = 'property.property'
    _description = 'Real estate properties model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Property Name', required=True)
    seller_id = fields.Many2one(
        'res.partner',
        string='Seller',
        domain=[('is_seller', '=', True)]
    )
    description = fields.Text(string='Description')

    stage_id = fields.Many2one(
        'property.stage', string='Stage', index=True, tracking=True,
        compute='_compute_stage_id', readonly=False, store=True,
        copy=False, group_expand='_read_group_stage_ids')
    tag_ids = fields.Many2many(
        'property.tag', string='Tags',
        help="Classify and analyze your Properties categories like: Training, Service")
    color = fields.Integer('Color Index', default=0)

    # Address
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")

    # Geo
    partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))

    # Main fields
    price = fields.Float(string='Price', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    area_sqft = fields.Float(string='Area (sq ft)')
    bedrooms = fields.Integer(string='Bedrooms')
    bathrooms = fields.Integer(string='Bathrooms')
    flooring_type = fields.Many2one('property.floor.type',string="Flooring Type")
    facing_direction = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
        ('northeast', 'North-East'),
        ('northwest', 'North-West'),
        ('southeast', 'South-East'),
        ('southwest', 'South-West'),
    ], string="Facing Direction")


    available_from = fields.Date(string='Available From')
    is_available = fields.Boolean(string='Is Available', default=True)
    furnishing = fields.Selection([
        ('unfurnished', 'Unfurnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('fully_furnished', 'Fully Furnished'),
    ], string="Furnishing")
    property_status = fields.Selection([
        ('new', 'New'),
        ('resale', 'Resale'),
        ('under_construction', 'Under Construction'),
    ], string="Property Status")
    year_built = fields.Integer(string="Year Built")
    total_floors = fields.Integer(string="Total Floors in Building")
    loan_available = fields.Boolean(string="Loan Available")

    # Images
    main_image = fields.Image(string='Main Image')
    additional_image_ids = fields.One2many('property.image', 'property_id', string='Additional Images')
    amenity_ids = fields.Many2many(
        'property.amenity',
        string="Amenities"
    )
    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env['property.stage'].search([])

    def _stage_find(self, limit=1):
        return self.env['property.stage'].search([()], limit=limit)


