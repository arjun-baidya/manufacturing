from odoo import fields, models, api, _, SUPERUSER_ID


class WorkSheet(models.Model):
    _name = 'mrp.work.sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Work Sheet"

    name = fields.Char('#Master work sheet', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    master_work_sheet_id = fields.Many2one('mrp.master.worksheet', string="Master Work Sheet")
    work_center_name = fields.Selection([('cutting', 'Cutting'), ('skyving', 'Skyving'), ('assemble', 'Assemble')], )
    state = fields.Selection(
        [('cutting', 'Cutting'), ('skiving', 'Skiving'), ('assemble', 'Assemble'),
         ('done', 'Done')])
    work_sheet_line_ids = fields.One2many('mrp.work.sheet.line', 'work_sheet_line_id', string="ids")
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)

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

    @api.onchange('work_sheet_line_ids', 'work_center_name')
    def onchange_type(self):
        for rec in self:
            for line in rec.work_sheet_line_ids:
                if rec.work_center_name == 'cutting':
                    line.cutting = True
                    line.skiving = False
                    line.assemble = False
                elif rec.work_center_name == 'skyving':
                    line.skiving = True
                    line.assemble = False
                    line.cutting = False
                elif rec.work_center_name == 'assemble':
                    line.assemble = True
                    line.skiving = False
                    line.cutting = False

    def cutting_confirm(self):
        for record in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('manufacturing_process.manufacturing_process_user_access')
            for u in grp.users:
                print(u.partner_id.name)
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                record.message_post(body="You have been assigned to next step.",
                                    partner_ids=partner_ids)
            record.state = 'skyving'

    def skiving_confirm(self):
        for rec in self:
            rec.state = 'assemble'

    def assemble_confirm(self):
        for rec in self:
            rec.state = 'done'


class WorkSheetLine(models.Model):
    _name = 'mrp.work.sheet.line'
    _description = "Work Sheet Line"

    material = fields.Char(string="Materials")
    part_name = fields.Char(string="Part Name")
    cutting_pending = fields.Integer(string="Cutting Pending")
    cutting_done = fields.Integer(string="Cutting Done")
    cutting = fields.Boolean()
    skiving_pending = fields.Integer(string="Skiving Pending")
    skiving_done = fields.Integer(string="Skiving Done")
    skiving = fields.Boolean()
    assemble_pending = fields.Integer(string="Assemble Pending")
    assemble_done = fields.Integer(string="Assemble Done")
    assemble = fields.Boolean()
    work_sheet_line_id = fields.Many2one('mrp.work.sheet', string="id")
