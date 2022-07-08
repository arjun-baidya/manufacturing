from odoo import fields, models, api, _


class BomInherit(models.Model):
    # _name = 'bom.inherit'
    _inherit = 'mrp.bom'
    _description = "base bom inherit"

    merchandising_sheet_id = fields.Many2one("merchandising.sheet", string='Merchandising Sheet', ondelete='cascade',
                                             default=lambda self: self.env.context.get('merchandising_sheet_id'))

    def action_view_bom(self):
        res = self.env.ref('mrp.mrp_bom_form_view')

        result = {'name': _('BOM'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'mrp.bom',
                  'type': 'ir.actions.act_window',
                  'target': 'current',
                  'res_id': self.id}
        return result
