from odoo import fields, models, api, _


class WorkSheet(models.Model):
    _name = 'mrp.work.sheet'

    _description = "Work Sheet"

    name = fields.Char('#Master work sheet', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    master_work_sheet_id = fields.Many2one('mrp.master.worksheet', string="Master Work Sheet")
    work_center_name = fields.Selection([('cutting', 'Cutting'), ('skyving', 'Skyving'), ('assemble', 'Assemble')],
                                        default='cutting')
    work_sheet_line_ids = fields.One2many('mrp.work.sheet.line', 'work_sheet_line_id', string="ids")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('work.sequence') or _('New')
        result = super(WorkSheet, self).create(vals)
        return result

    @api.onchange('master_work_sheet_id')
    def onchange_line_create(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.master_work_sheet_id.master_worksheet_line_ids:
                val = {
                    'material': line.material_name,
                    'part_name': line.part_name,
                    'cutting_pending': line.cutting_pending,
                    'skiving_pending': line.skiving_pending,
                    'assemble_pending': line.assemble_pending,
                }
                lines.append((0, 0, val))
            rec.work_sheet_line_ids = lines


class WorkSheetLine(models.Model):
    _name = 'mrp.work.sheet.line'
    _description = "Work Sheet Line"

    material = fields.Char(string="Materials")
    part_name = fields.Char(string="Part Name")
    cutting_pending = fields.Integer(string="Cutting Pending")
    cutting_done = fields.Integer(string="Cutting Done")
    skiving_pending = fields.Integer(string="Skiving Pending")
    skiving_done = fields.Integer(string="Skiving Done")
    assemble_pending = fields.Integer(string="Assemble Pending")
    assemble_done = fields.Integer(string="Assemble Done")
    work_sheet_line_id = fields.Many2one('mrp.work.sheet', string="id")
