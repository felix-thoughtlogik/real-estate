from odoo import http
from odoo.http import request

class WebsiteController(http.Controller):

    @http.route(['/video/<string:video_name>'], type='http', auth='public', website=True)
    def home_page(self, video_name):
        return request.render('real_estate_website.video_page', {'video_name': video_name})
