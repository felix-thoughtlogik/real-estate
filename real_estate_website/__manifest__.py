{
    'name': 'Real Estate Website',
    'version': '1.1.0',
    'summary': 'Manage real estate website, leads, properties',
    'description': """
Real Estate Management for Odoo 
- Dealer contact access control
- Property and customer management
    """,
    'author': 'Felix Hilbert',
    'website': 'https://yourwebsite.com',
    'category': 'Sales/CRM',
    'depends': ['base','website'],
    'data': [
        'security/ir.model.access.csv',  
        'views/properties_templates.xml',
    ],
    'assets':{
        'web.assets_frontend':[
            'real_estate_website/static/css/home_page.css'
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
