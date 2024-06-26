from odoo import fields, models, api, _


class BomInherit(models.Model):
    _inherit = 'mrp.bom'
    # _rec_name = 'name'
    _parent_name = 'name_id'

    md_sheet_id = fields.Many2one('merchandising.sheet', string="MD id")
    name_id = fields.Char('BOM', required=True, readonly=True, index=True, default=lambda self: _('New'))
    net_qty = fields.Selection([('net_loss', "Net Loss"), ('net_buyer', "Net Buyer"), ('net_purchase', "Net Purchase")])

    def name_get(self):
        result = []
        for rec in self:
            # name = rec.name_id
            result.append((rec.id, str(rec.name_id)))
            # result.append((rec.name_id, name))
        return result

    @api.model
    def create(self, vals):
        if vals.get('name_id', _('New')) == _('New'):
            vals['name_id'] = self.env['ir.sequence'].next_by_code('bom.sequence') or _('New')
        result = super(BomInherit, self).create(vals)
        return result

    @api.onchange('md_sheet_id', 'net_qty')
    def onchange_line_create(self):
        for i in self.ids:
            current_bom_id = i
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.md_sheet_id.order_line:
                if line.bom_no.id == current_bom_id and rec.net_qty == 'net_loss':
                    val = {
                        'product_id': line.product_id,
                        'product_qty': line.net_loss,
                    }
                    lines.append((0, 0, val))
                elif line.bom_no.id == current_bom_id and rec.net_qty == 'net_buyer':
                    val = {
                        'product_id': line.product_id,
                        'product_qty': line.net_buyer,
                    }
                    lines.append((0, 0, val))
                elif line.bom_no.id == current_bom_id and rec.net_qty == 'net_purchase':
                    val = {
                        'product_id': line.product_id,
                        'product_qty': line.net_purchase,
                    }
                    lines.append((0, 0, val))
            rec.bom_line_ids = lines

    # def merge_duplicate_product_in_bom(self):
    #     if self.bom_line_ids:
    #         for line in self.bom_line_ids:
    #             if line.id in self.bom_line_ids.ids:
    #                 line_ids = self.bom_line_ids.filtered(lambda m: m.product_id == line.product_id)
    #                 quantity = 0
    #                 for qty in line_ids:
    #                     quantity += qty.product_qty
    #                 line_ids[0].write({'product_qty': quantity,
    #                                    'product_id': line_ids[0].product_id})
    #                 line_ids[1:].unlink()
