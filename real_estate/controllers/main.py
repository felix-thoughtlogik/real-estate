from odoo import http
from odoo.http import request

class PropertiesController(http.Controller):

    @http.route([
        '/properties',
        '/properties/category/<string:category_slug>',
        '/properties/<string:property_slug>'
    ], type='http', auth='public', website=True)
    def properties_page(self, category_slug=None, property_slug=None):
        Property = request.env['property.property']
        Category = request.env['property.category']
        all_properties = Property.search([])

        if property_slug:
            prop = Property.search([('slug', '=', property_slug)], limit=1)
            if prop:
                return request.render('real_estate.property_details', {'property': prop})
            return request.render('real_estate.property_list', {
                'properties': all_properties,
                'not_found': True,
                'not_found_type': 'property'
            })

        if category_slug:
            cat = Category.search([('slug', '=', category_slug)], limit=1)
            if cat:
                props = Property.search([('sub_category_id', '=', cat.id)])
                return request.render('real_estate.property_list', {
                    'properties': props + (all_properties - props),
                    'category': cat
                })
            return request.render('real_estate.property_list', {
                'properties': all_properties,
                'not_found': True,
                'not_found_type': 'category'
            })

        return request.render('real_estate.property_list', {
            'properties': all_properties
        })
