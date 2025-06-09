{
    'name': 'Real Estate Management',
    'version': '1.1.0',
    'summary': 'Manage real estate properties, sellers, and customer contacts',
    'description': """
Real Estate Management for Odoo Community
- CRM Integration
- Dealer contact access control
- Property and customer management
    """,
    'author': 'Felix',
    'website': 'https://yourwebsite.com',
    'category': 'Sales/CRM',
    'depends': ['base', 'crm', 'contacts','website','theme_real_estate'],
    'data': [
        # 'security/security.xml',  # Security rules, e.g., user permissions
        'security/ir.model.access.csv',  # Your access control list (ACL) file if needed
        'views/properties_views.xml',
        'views/properties_stages_views.xml',
        'views/properties_seller_views.xml',
        'views/properties_category_views.xml',
        'views/crm_lead.xml',
        'views/website_properties_menu.xml',
        'views/website_properties_templates.xml',
        'data/properties_stage_data.xml',
        'data/property_category_data.xml',
        'views/menu.xml',
    ],
    'assets':{
        'web.assets_frontend':[
            'real_estate/static/css/property_page.css'
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
