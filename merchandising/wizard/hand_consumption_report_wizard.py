from odoo import fields, models, api


class HandConsumptionReportWizard(models.TransientModel):
    _name = 'hand.consumption.report.wizard'
    _description = "Hand consumption report wizard"

    style_no = fields.Char(string="Style")

    def action_report_print(self):
        data = {
                # 'form_data': self.read()[0],
                'model': 'hand.consumption.report.wizard',
                'form': self.read()[0],
            }
        merchandising_data = self.env['merchandising.sheet'].search([('style_no', '=', self.style_no)])
        merchandising = []
        for rec in merchandising_data:
            vals = {
                'style_no': rec.style_no,
            }
            merchandising.append(vals)
        data['merchandising_data'] = merchandising
        print('data :', data['merchandising_data'])
        return self.env.ref('merchandising.report_filter_hand_consumption').report_action(self, data=merchandising)
