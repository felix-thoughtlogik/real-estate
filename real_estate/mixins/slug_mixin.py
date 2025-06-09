import re
from odoo import api, fields, models

def to_snake_case(text):
    # Remove any non-word characters except spaces
    cleaned = re.sub(r'[^\w\s]', '', text)
    # Split by whitespace
    words = cleaned.strip().split()
    # Join with underscore and lowercase all
    return '-'.join(word.lower() for word in words)

class SlugMixin(models.AbstractModel):
    _name = 'slug.mixin'
    _description = 'Slug Mixin for lowerCamelCase slug field'

    slug = fields.Char(string='Slug', compute='_compute_slug', index=True)

    @api.depends('name')
    def _compute_slug(self):
        for rec in self:
            rec.slug = f"{to_snake_case(rec.name or '')}-{rec.id}"