from odoo import fields, models, api, _


class ManufacturingOrder(models.Model):
    _inherit = 'stock.move'
    _description = "base bom inherit"

    merchandising_sheet_id = fields.Many2one("merchandising.sheet", string='Merchandising Sheet', ondelete='cascade',
                               default=lambda self: self.env.context.get('merchandising_sheet_id'))

    def action_view_manufacturing(self):
        res = self.env.ref('mrp.mrp_production_form_view')
        result = {'name': _('manufacturing'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'mrp.production',
                  'type': 'ir.actions.act_window',
                  'target': 'current',
                  'res_id': self.id}
        return result
