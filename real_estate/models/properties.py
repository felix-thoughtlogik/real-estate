from odoo import api, fields, models


class PropertiesTags(models.Model):
    _name = 'property.tag'
    _description = 'Real Estate Property Tags'
    _rec_name = 'name'
    _inherit = ['slug.mixin']

    name = fields.Char(string='Type Name', required=True)
    description = fields.Text(string='Description')

class PropertyStage(models.Model):

    _name = "property.stage"
    _description = "Properties Stages"
    _rec_name = 'name'
    _order = "sequence, name, id"
    _inherit = ['slug.mixin']

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    is_won = fields.Boolean('Is Won Stage?')
    requirements = fields.Text('Requirements', help="Enter here the internal requirements for this stage (ex: Offer sent to customer). It will appear as a tooltip over the stage's name.")

    fold = fields.Boolean('Folded in Pipeline',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')

class PropertyImage(models.Model):
    _name = 'property.image'
    _description = 'Additional Images for Properties'
    _inherit = ['slug.mixin']

    name = fields.Char(string='Description')
    image = fields.Image(string='Image')
    property_id = fields.Many2one('property.property', string='Property', required=True)

class PropertyAmenity(models.Model):
    _name = 'property.amenity'
    _description = 'Property Amenity'
    _inherit = ['slug.mixin']

    name = fields.Char(string="Amenity Name", required=True)
    icon = fields.Char(string="Icon")
    description = fields.Text(string='Description')

class PropertyFloorType(models.Model):
    _name = 'property.floor.type'
    _description = 'Property Floor Type'
    _inherit = ['slug.mixin']

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string='Description')

class PropertyCategory(models.Model):
    _name = 'property.category'
    _inherit = ['slug.mixin']

    name = fields.Char(string="Name")
    is_submenu = fields.Boolean(string='Is Submenu', compute='_compute_is_submenu',store=True, default=False)
    parent_id = fields.Many2one(
        string='Parent Category',
        comodel_name='property.category',
    )
    sub_category_ids = fields.One2many(string='Sub Categories', comodel_name='property.category', inverse_name='parent_id')
    description = fields.Text(string='Description')

    @api.model
    def default_get(self, fields_list):
        defaults = super(PropertyCategory, self).default_get(fields_list)
        if self.env.context.get('default_parent_id'):
            defaults['parent_id'] = self.env.context['default_parent_id']
        return defaults

    @api.depends('parent_id')
    def _compute_is_submenu(self):
        for record in self:
            record.is_submenu = bool(record.parent_id)


class RealEstateProperties(models.Model):
    _name = 'property.property'
    _description = 'Real estate properties model'
    _inherit = ['mail.thread', 'mail.activity.mixin','slug.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Property Name', required=True)
    seller_id = fields.Many2one(
        'res.partner',
        string='Seller',
        domain=[('is_seller', '=', True)],
        required=True
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
    category_id =  fields.Many2one(string='Category',comodel_name='property.category', domain="[('is_submenu','=',False)]",required = True)
    sub_category_id = fields.Many2one(string='Sub Category',comodel_name='property.category',required = True)
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


