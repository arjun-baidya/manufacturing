# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Merchandising',
    'version': '15.0.1.0.0',
    'category': 'merchandising',
    'description': """
        This is custom merchandising Info
    """,
    'summary': ' ',
    'website': 'https://www.pisoftwareltd.com/',
    'depends': [
            'sale_management',
            'sale',
            'hr',
            'hr_contract',
            'mrp',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/merchandising_sequence.xml',
        'views/merchandising_sheet.xml',
        'views/pattern_cut.xml',
        'wizard/hand_consumption_report_wizard.xml',
        'report/hand_consumption.xml',
        'report/hand_consumption_report_filter.xml',
        'report/pattern_cut_report.xml',
        'report/combination_report.xml',
        'report/buyer_estimate_report.xml',
        'report/estimate_sheet_report.xml',
        'report/distribution_report.xml',
        'report/pattern_cut_lebel_report.xml',
        'report/report.xml',
        'views/menu_items.xml',

    ],
    'installable': True,
    'application': True,
}
