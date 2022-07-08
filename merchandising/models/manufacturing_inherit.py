from odoo import fields, models, api


class ManufacturingInherit(models.Model):
    _inherit = 'mrp.production'

    md_sheet_id = fields.Many2one('merchandising.sheet', string="MD Sheet")

    @api.onchange('md_sheet_id')
    def onchange_product(self):
        self.product_id = self.md_sheet_id.product
