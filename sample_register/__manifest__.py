# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sample Register',
    'version': '15.0.1.0.0',
    'category': 'Services',
    'description': """
        This is custom module for document register
    """,
    'summary': ' ',
    'website': 'https://www.pisoftwareltd.com/',
    'depends': [
            'base',
            'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/sample_document_register.xml'
    ],
    'installable': True,
    'application': True,
}
