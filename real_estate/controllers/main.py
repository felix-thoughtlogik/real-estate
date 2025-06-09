from odoo import http
from odoo.http import request


class PropertiesController(http.Controller):

    @http.route(['/properties','/properties/<string:slug>'],type='http',methods=['GET'],website = True)
    def properties_page(self,slug= None):
        if slug:
            return request.render('real_estate.property_lists', {})
        else:
            return request.render('real_estate.property_details',{})
