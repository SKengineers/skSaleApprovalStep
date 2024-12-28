# -*- coding: utf-8 -*-
{
    'name': "SK odoo Sale Approval Step",
    'summary': """
        Sale Approval Step For Sale Order""",
    'description': """
        Sale Approval Step For Sale Order
            """,
    'author': 'Sritharan K',
    'company': 'SK Engineer',
    'maintainer': 'SK Engineer',
    'website': "https://www.skengineer.be",
    'category': 'Sales',
    'version': '17.1',
    'depends': ['base', 'sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',

        'views/res_config_setting_view.xml',
        'views/sale_order_view.xml',

        'wizards/sale_order_reject_view.xml',
    ],
    'images': [
        '/static/description/icon.png',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
