from odoo import fields, models, api, _
from datetime import datetime, timedelta, date


class SamplePatternCut(models.Model):
    _name = 'sample.pattern.cut'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = " handover designer for pattern cut"
    _parent_name = "parent_id"
    _rec_name = 'name'

    @api.depends('pattern_cut_line_ids', 'pattern_cut_line_ids.pcs')
    def compute_total_pcs(self):
        for rec in self:
            total = 0
            for line in rec.pattern_cut_line_ids:
                total += line.pcs
            rec['total_pcs'] = total

    name = fields.Char('PID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    received_name = fields.Many2one('hr.employee', string="Receiver")
    series_name = fields.Char(string="Series Name")
    style_no = fields.Char(string="Style No")
    customer_name = fields.Char(string="Customer Name")
    received_date = fields.Date(string="Received Date")
    pattern_qty = fields.Integer(string="Pattern Qty")
    target_date = fields.Date(string="Target Date")
    start_time = fields.Datetime(string="Start Time")
    end_time = fields.Datetime(string="End Time")
    pattern_cut_duration = fields.Float(compute='_compute_pattern_duration', string="Duration(Hour)")
    product = fields.Many2one('product.template', string="Product")
    total_pcs = fields.Integer(string="Total PCS", compute='compute_total_pcs', store=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('pattern_start', 'Pattern Start'),
                              ('pattern_end', 'Pattern End'),
                              ], default='draft',
                             track_visibility='onchange')
    # link to md sheet for
    merchandising_sheet_id = fields.Many2one("merchandising.sheet", string='Merchandising Sheet', ondelete='cascade',
                                             readonly=True,
                                             default=lambda self: self.env.context.get('merchandising_sheet_id'))
    pattern_cut_line_ids = fields.One2many('pattern.cut.line', 'patten_cut_id', string="pattern cut ids")

    parent_id = fields.Many2one('sample.pattern.cut', 'parent id', index=True, ondelete='cascade')

    def merge_duplicate_type(self):
        if self.pattern_cut_line_ids:
            for line in self.pattern_cut_line_ids:
                if line.id in self.pattern_cut_line_ids.ids:
                    line_ids = self.pattern_cut_line_ids.filtered(lambda m: m.type == line.type)
                    quantity = 0
                    for qty in line_ids:
                        quantity += qty.pcs
                    line_ids[0].write({'pcs_for_report': quantity,
                                       'type_for_report': line_ids[0].type})
                    # line_ids[1:].unlink()

    def _generate_categories(self, categories, pattern):
        categories.append(pattern)
        for cat in self.search([('parent_id', '=', pattern)]):
            categories = self._generate_categories(categories, cat.id)
        return categories

    def get_categories(self, pattern):
        categories = []
        categories = self._generate_categories(categories, pattern)
        return categories

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('pattern.cut.sequence') or _('New')
        result = super(SamplePatternCut, self).create(vals)
        return result

    def pattern_start_btn(self):
        for rec in self:
            rec.state = 'pattern_start'
            if rec.state == 'pattern_start':
                rec.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def sample_pattern_cancel(self):
        if self.state == 'pattern_start':
            self.start_time = 0
            for rec in self:
                rec.state = 'draft'

    def pattern_end_btn(self):
        for rec in self:
            rec.state = 'pattern_end'
            if rec.state == 'pattern_end':
                rec.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @api.depends('start_time', 'end_time')
    def _compute_pattern_duration(self):
        if self.end_time:
            tot_sec = (self.end_time - self.start_time).total_seconds()
            self.pattern_cut_duration = round(tot_sec / 60)
        else:
            self.pattern_cut_duration = 0.0

    def action_view_pattern_cut(self):
        res = self.env.ref('merchandising.sample_pattern_cut_form_view')
        result = {'name': _('Pattern Cut'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'sample.pattern.cut',
                  'type': 'ir.actions.act_window',
                  'target': 'current',
                  'res_id': self.id}
        return result


class PatternCutLine(models.Model):
    _name = 'pattern.cut.line'
    _rec_name = 'pattern'
    _description = "Pattern Cut Line model"

    pattern = fields.Char(string="Part Name")
    type = fields.Selection([('leather', "Leather"), ('lining', "Lining"), ('rf', "Reinforcement"), ('netto', "Netto")])
    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    pcs = fields.Integer(string="PCS")
    size = fields.Integer(string="Size")
    uom = fields.Many2one('uom.uom', string="UOM")
    loss_percentage = fields.Float(string="Loss %")
    # for report some extra field initialize
    type_for_report = fields.Char()
    pcs_for_report = fields.Integer()
    ###################################
    patten_cut_id = fields.Many2one('sample.pattern.cut', string="pattern cut id")





