# -*- coding: utf-8 -*-
{
    'name': "HR Worning",

    'summary': """
        HR Worning""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_payroll'],

    # always loaded
    'data': [
        'security/security_view.xml',
        'security/ir.model.access.csv',
        'views/hr_worning.xml',
        'data/salary_rule_worning.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
