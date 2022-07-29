from odoo import fields, models, api


class ProductInherit(models.Model):
    _inherit = 'product.template'
    _description = "into product template initialize custom field"

    pattern_uom = fields.Many2one('uom.uom', string="Pattern UOM")
