from odoo import fields, models, api


class SalesOrderSheet(models.Model):
    # _name = 'saless.sample'
    _inherit = ["sale.order"]
    _description = "sample order model"
    _rec_name = 'series_name'

    series_name = fields.Char(string="Series Name")
    style_name = fields.Char(string="Style Name")
    # color_code = fields.Char(string="Color Code")
    delivery_date = fields.Date(string="Delivery Date")
    delivery_way = fields.Char(string="Delivery Way")
    total_sample_qty = fields.Integer(string="Total Sample Qty")

    def generate_md_sheet(self):
        self.ensure_one()
        inv_lines = []

        for line_items in self.order_line:
            tmp = {
                "product_id": line_items.product_id.id,
                "product_qty": line_items.product_uom_qty,
                "price_unit": line_items.price_unit,
            }
            inv_lines.append([0, False, tmp])

        order_values = {
            'customer_name': self.partner_id.name,
            'series_name': self.series_name,
            'style_no': self.style_name,
            # 'color_code': self.color_code,
            'total_sample_qty': self.total_sample_qty,
            "order_line": inv_lines,
        }
        self.env['merchandising.sheet'].create(order_values)

    # def generate_md_sheet(self):
    #     ref_obj = self.env['merchandising.sheet']
    #     values = {
    #         'series_name': self.series_name,
    #         'style_no': self.style_name,
    #         'customer_name': self.partner_id.name,
    #         'product_name': self.order_line.product_id.name,
    #     }
    #     ref_obj.create(values)
