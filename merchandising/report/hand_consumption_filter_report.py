from odoo import fields, models, api


class HandConsumptionFilterReport(models.AbstractModel):
    _name = 'report.merchandising.filter_report_hand_consumption_id'

    @api.model
    def _get_report_values(self, docids, data):
        merchandising_data = self.env['merchandising.sheet'].search([('style_no', '=', data['style'])])
        form_data = []
        for data in merchandising_data[0]:
            val = {
                'style_no': data.style_no,
                'series_no': data.series_name
            }
            form_data.append(val)
        print(form_data)
        merchandising = []
        for rec in merchandising_data:
            for line in rec.order_line:
                vals = {
                    'material': line.product_id.name,
                    'part_name': line.part_name.pattern,
                    'length': line.length,
                    'width': line.width,
                    'pcs': line.pcs,
                    'size': line.size,
                    'net': line.net,
                    'factory_loss': line.factory_loss,
                    'net_factory': line.net_loss,
                }
                merchandising.append(vals)
        return {
            'docs': merchandising_data,
            'data': data,
            'merchandising': merchandising,
            'form_data': form_data,
        }
