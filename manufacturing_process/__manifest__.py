# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Manufacturing Process',
    'version': '15.0.1.0.0',
    'category': 'Manufacturing',
    'description': """
        This is custom manufacturing Info
    """,
    'summary': ' ',
    'website': 'https://www.pisoftwareltd.com/',
    'depends': [
            'merchandising',
            'sale_management',
            'sale',
            'hr',
            'hr_contract',
            'mrp',
            'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/manufacturing_sequence.xml',
        'views/bom_inherit.xml',
        'views/manufacturing_inherit.xml',
        'views/master_worksheet.xml',
        'views/work_sheet.xml',
        'views/product_inherit.xml',
        'views/menu_items.xml',
    ],
    'installable': True,
    'application': True,
}
