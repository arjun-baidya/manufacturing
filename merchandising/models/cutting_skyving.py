from odoo import fields, models, api, _
from datetime import datetime, timedelta, date


class SampleCuttingSkyving(models.Model):
    _name = 'sample.cutting.skyving'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Sample cutting and skyving model"
    # _rec_name = 'series_name'

    md_sheet_no = fields.Many2one('merchandising.sheet', string="MD Sheet No")
    total_sample_qty = fields.Char(string="Total Sample Qty")
    sample_cutting_man = fields.Many2one('hr.employee', string="Cutting Man")
    cutting_start_time = fields.Datetime(string="Cutting Start")
    cutting_end_time = fields.Datetime(string="Cutting End")
    cutting_time_result = fields.Float(compute='_compute_cutting_duration', string="Cutting Time")
    skyving_start_time = fields.Datetime(string="Skyving Start")
    skyving_end_time = fields.Datetime(string="Skyving End")
    skyving_time_result = fields.Float(compute='_compute_skyving_duration', string="Skyving Time")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cutting_start', 'Cutting Start'),
        ('cutting_end', 'Cutting End'),
        ('skyving_start', 'Skyving Start'),
        ('skyving_end', 'Skyving End'),
    ], default='draft', track_visibility='onchange')
    sample_cutting_skyving_line_ids = fields.One2many('sample.cutting.skyving.line', 'sample_cutting_skyving_id',
                                                      string="line ids")
    # link to md sheet for
    merchandising_sheet_id = fields.Many2one("merchandising.sheet", string='Merchandising Sheet', ondelete='cascade',
                                             readonly=True,
                                             default=lambda self: self.env.context.get('merchandising_sheet_id'))

    @api.onchange('md_sheet_no')
    def onchange_cutiing_skyving(self):
        self.total_sample_qty = self.md_sheet_no.total_sample_qty

    def sample_cutting_start(self):
        for rec in self:
            rec.state = 'cutting_start'
            if rec.state == 'cutting_start':
                rec.cutting_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def sample_cutting_cancel(self):
        if self.state == 'cutting_start':
            self.cutting_start_time = 0
            for rec in self:
                rec.state = 'draft'

    def sample_cutting_stop(self):
        for rec in self:
            rec.state = 'cutting_end'
            if rec.state == 'cutting_end':
                rec.cutting_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @api.depends('cutting_start_time', 'cutting_end_time')
    def _compute_cutting_duration(self):
        if self.cutting_end_time:
            tot_sec = (self.cutting_end_time - self.cutting_start_time).total_seconds()
            self.cutting_time_result = round(tot_sec / 60)
        else:
            self.cutting_time_result = 0.0

    def sample_skyving_start(self):
        for rec in self:
            rec.state = 'skyving_start'
            if rec.state == 'skyving_start':
                rec.skyving_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def sample_skyving_cancel(self):
        if self.state == 'skyving_start':
            self.skyving_start_time = 0
            for rec in self:
                rec.state = 'draft'

    def sample_skyving_stop(self):
        for rec in self:
            rec.state = 'skyving_end'
            if rec.state == 'skyving_end':
                rec.skyving_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @api.depends('skyving_start_time', 'skyving_end_time')
    def _compute_skyving_duration(self):
        if self.skyving_end_time:
            tot_sec = (self.skyving_end_time - self.skyving_start_time).total_seconds()
            self.skyving_time_result = round(tot_sec / 60)
        else:
            self.skyving_time_result = 0.0

    # it is for back  sample_cutting_skyving_form_view this view from md sheet view
    def action_view_cutting_skyving(self):
        res = self.env.ref('merchandising.sample_cutting_skyving_form_view')
        result = {'name': _('Cutting Skyving'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'sample.cutting.skyving',
                  'type': 'ir.actions.act_window',
                  'target': 'current',
                  'res_id': self.id}
        return result


class SampleCuttingSkyvingLine(models.Model):
    _name = 'sample.cutting.skyving.line'
    _description = "sample cutting skyving line models"

    product_name = fields.Many2one('product.product', string="Product Name")
    product_des = fields.Char(string="Product Description")
    product_qty = fields.Integer(string="Product Qty")
    sample_cutting_skyving_id = fields.Many2one('sample.cutting.skyving', string="Cutting Skyving Id")
