{
    'name': 'Real Estate Management',
    'version': '1.1.0',
    'summary': 'Manage real estate properties, dealers, and customer contacts',
    'description': """
Real Estate Management for Odoo Community
- CRM Integration
- Dealer contact access control
- Property and customer management
    """,
    'author': 'Felix',
    'website': 'https://yourwebsite.com',
    'category': 'Sales/CRM',
    'depends': ['base', 'crm', 'contacts'],
    'data': [
        'security/security.xml',  # Security rules, e.g., user permissions
        'security/ir.model.access.csv',  # Your access control list (ACL) file if needed
        'views/properties_views.xml',
        'views/properties_stages.xml',
        'views/crm_views.xml',
        'data/properties_stage_data.xml',

        'wizard/convert_company_user.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
