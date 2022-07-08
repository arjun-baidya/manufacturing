from odoo import fields, models, api, _


class MasterWorkSheet(models.Model):
    _name = 'mrp.master.worksheet'
    _description = "Master Work sheet"

    name = fields.Char('#Master work sheet', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    md_sheet_id = fields.Many2one('merchandising.sheet', string="Md Sheet")
    manufacturing_order_id = fields.Many2one('mrp.production', string="Manufacturing Order")
    quantity = fields.Integer(string="Quantity")
    master_worksheet_line_ids = fields.One2many('mrp.master.worksheet.line', 'master_worksheet_line_id', string="ids")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('master.work.sequence') or _('New')
        result = super(MasterWorkSheet, self).create(vals)
        return result

    @api.onchange('md_sheet_id')
    def onchange_line_create(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.md_sheet_id.order_line:
                val = {
                    'material_name': line.product_id.name,
                    'part_name': line.part_name.pattern,
                    'pcs': line.pcs,
                    'qty': rec.quantity,
                }
                lines.append((0, 0, val))
            rec.master_worksheet_line_ids = lines

    @api.onchange('manufacturing_order_id')
    def onchange_qty(self):
        self.quantity = self.manufacturing_order_id.product_qty

    def data_get(self):
        data = self.env['mrp.work.sheet'].search([('master_work_sheet_id', '=', self.name)])
        for datas in data.work_sheet_line_ids:
            print(datas.material, datas.cutting_done)
        for rec in self.master_worksheet_line_ids:
            rec.cutting_done = datas.cutting_done


class MaterWorkSheetLine(models.Model):
    _name = 'mrp.master.worksheet.line'
    _description = "Mater work sheet line"

    material_name = fields.Char(string="Material")
    part_name = fields.Char(string="Part Name")
    pcs = fields.Integer(string="PCS")
    qty = fields.Integer(string="Qty")
    total = fields.Integer(string="Total", compute='calc_total')
    cutting_pending = fields.Integer(string="Cutting Pending", compute='calc_cutting_pending')
    cutting_done = fields.Integer(string="Cutting Done")
    skiving_pending = fields.Integer(string="Skiving Pending")
    skiving_done = fields.Integer(string="Skiving Done")
    assemble_pending = fields.Integer(string="Assemble Pending")
    assemble_done = fields.Integer(string="Assemble Done")
    master_worksheet_line_id = fields.Many2one('mrp.master.worksheet', string="id")

    @api.depends('pcs', 'qty')
    def calc_total(self):
        for rec in self:
            rec.total = rec.pcs * rec.qty

    @api.depends('total')
    def calc_cutting_pending(self):
        for rec in self:
            rec.cutting_pending = rec.total - rec.cutting_done
            rec.skiving_pending = rec.total - rec.skiving_done
            rec.assemble_pending = rec.total - rec.assemble_done
