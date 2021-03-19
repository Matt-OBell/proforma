# -*- coding: utf-8 -*-
{
    'name': "pro-forma",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Opeyemi Adeyemi",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', "account_invoicing"],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/report.xml',
        "data/email_template.xml",
        'reports/proreport.xml',
        "views/sequence.xml",
        "views/proforma.xml",
    ],
}