from odoo import fields, models, api


class AllConsumptionReportWizard(models.TransientModel):
    _name = 'all.consumption.report.wizard'
    _description = "All consumption report wizard"

    style_no = fields.Char(string="Style")
    manufacturing_order = fields.Many2many('mrp.production', string="Manufacturing Order")
    all_consumption_line_ids = fields.One2many('all.consumption.line', 'all_consumption_line_id', string="ids")

    def action_report_print(self):
        data = {}
        data['style'] = self.style_no
        return self.env.ref('merchandising.report_all_consumption').report_action(None, data=data)

    @api.onchange('manufacturing_order')
    def onchange_line_create(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.manufacturing_order.move_raw_ids:
                val = {
                    'materials': line.product_id.name,
                    'consume': line.quantity_done,
                }
                lines.append((0, 0, val))
            rec.all_consumption_line_ids = lines

    def merge_duplicate_line(self):
        if self.all_consumption_line_ids:
            for line in self.all_consumption_line_ids:
                if line.id in self.all_consumption_line_ids.ids:
                    line_ids = self.all_consumption_line_ids.filtered(lambda m: m.materials == line.materials)
                    quantity = 0
                    for qty in line_ids:
                        quantity += qty.consume
                    line_ids[0].write({'consume': quantity,
                                       'materials': line_ids[0].materials})
                    line_ids[1:].unlink()
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'all.consumption.report.wizard',
            'target': 'new',
            'res_id': self.id
        }


class AllConsumptionLine(models.TransientModel):
    _name = 'all.consumption.line'

    manufac_order = fields.Char(string="MO")
    materials = fields.Char(string="Materials")
    consume = fields.Integer(string="Consume")
    all_consumption_line_id = fields.Many2one('all.consumption.report.wizard', 'id')
