from odoo import fields, models, api


class ManufacturingInherit(models.Model):
    _inherit = 'mrp.production'

    md_sheet_id = fields.Many2one('merchandising.sheet', string="MD Sheet")
    style_no = fields.Char(string="Style")
    series_name = fields.Char(string="Series")
    buyer_name = fields.Char(string="Buyer Name")

    @api.onchange('md_sheet_id')
    def onchange_product(self):
        self.product_id = self.md_sheet_id.product

    @api.onchange('md_sheet_id')
    def onchange_md_sheet_wise(self):
        self.style_no = self.md_sheet_id.style_no
        self.series_name = self.md_sheet_id.series_name
        self.buyer_name = self.md_sheet_id.customer_name.name
