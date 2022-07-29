from odoo import fields, models, api


class AllConsumptionReport(models.AbstractModel):
    _name = 'report.merchandising.all_consumption_report_template'

    # if self.env.context.get('active_id'):
    #     departure_date = self.env['hr.employee'].browse(self.env.context['active_id'])
    @api.model
    def _get_report_values(self, docids, data):
        manufacturing_data = self.env['mrp.production'].search([('style_no', '=', data['style'])])
        if self.env.context.get('active_id'):
            merge_data = self.env['all.consumption.report.wizard'].browse(self.env.context['active_id'])
            merge_datas = []
            for merge in merge_data.all_consumption_line_ids:
                val = {
                    'materials': merge.materials,
                    'consume': merge.consume,
                }
                merge_datas.append(val)
        form_data = []
        for data in manufacturing_data[0]:
            val = {
                'style_no': data.style_no,
                'series_no': data.series_name,
                'buyer_name': data.buyer_name,
            }
            form_data.append(val)
        manufacturing = []
        for rec in manufacturing_data:
            for line in rec.move_raw_ids:
                vals = {
                    'id': line.id,
                    'product': rec.product_id.name,
                    'materials': line.product_id.name,
                    'product_uom_qty': line.product_uom_qty,
                    'quantity_done': line.quantity_done,
                }
                manufacturing.append(vals)
        return {
            'docs': manufacturing_data,
            'data': data,
            'manufacturing': manufacturing,
            'form_data': form_data,
            'merge_datas': merge_datas,
        }
