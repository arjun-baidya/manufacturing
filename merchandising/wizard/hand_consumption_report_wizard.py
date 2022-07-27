from odoo import fields, models, api


class HandConsumptionReportWizard(models.TransientModel):
    _name = 'hand.consumption.report.wizard'
    _description = "Hand consumption report wizard"

    style_no = fields.Char(string="Style")

    def action_report_print(self):
        data = {}
        data['style'] = self.style_no
        return self.env.ref('merchandising.report_filter_hand_consumption').report_action(None, data=data)

