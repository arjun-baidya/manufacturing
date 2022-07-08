from odoo import fields, models, api, _


class PatternRegister(models.Model):
    _name = 'pattern.register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = " Pattern Register model"
    _rec_name = 'series_name'

    serial_num = fields.Char('SL', required=True, copy=False, readonly=True, index=True,
                             default=lambda self: _('New'))
    series_name = fields.Char(string="Series Name")
    style_no = fields.Char(string="Style No")
    customer_name = fields.Char(string="Customer Name")
    receiver_name = fields.Many2one('hr.employee', string="Receiver Name")
    date = fields.Date(string="Date")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ], default='draft',
                             track_visibility='onchange')
    pattern_register_line_ids = fields.One2many('pattern.register.line', 'pattern_register_id',
                                                string="register line")
    # link to md sheet for
    merchandising_sheet_id = fields.Many2one("merchandising.sheet", string='Merchandising Sheet', ondelete='cascade',
                                             readonly=True,
                                             default=lambda self: self.env.context.get('merchandising_sheet_id'))
    # connect to md sheet for some data get
    mds_ids = fields.Many2many('merchandising.sheet', string='MD No')

    @api.model
    def create(self, vals):
        if vals.get('serial_num', _('New')) == _('New'):
            vals['serial_num'] = self.env['ir.sequence'].next_by_code('pattern.register.sequence') or _('New')
        result = super(PatternRegister, self).create(vals)
        return result

    @api.onchange('mds_ids')
    def onchange_mdto_pattern(self):
        self.series_name = self.mds_ids.series_name
        self.style_no = self.mds_ids.style_no
        self.customer_name = self.mds_ids.customer_name

    def pattern_register_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def pattern_register_cancel(self):
        for rec in self:
            rec.state = 'draft'

    # it is for back  pattern_register_form_view this view from md sheet view
    def action_view_pattern_register(self):
        res = self.env.ref('merchandising.pattern_register_form_view')
        result = {'name': _('Pattern Register'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'pattern.register',
                  'type': 'ir.actions.act_window',
                  'target': 'current',
                  'res_id': self.id}
        return result


class PatternRegisterLine(models.Model):
    _name = 'pattern.register.line'
    _description = " This is pattern register Line model"
    _rec_name = 'pattern_name'

    pattern_name = fields.Many2one('product.product', string="Pattern Name")
    pattern_details = fields.Char(string="Pattern Details")
    material_type = fields.Selection([('leather', 'Leather'), ('lining', 'Lining'), ('rf', 'RF')], string="Material Type")
    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    pattern_register_id = fields.Many2one('pattern.register', string="pattern register id")
