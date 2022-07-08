from odoo import fields, models, api, _


class SamplePatternCut(models.TransientModel):
    _name = 'sample.pattern.cut'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = " handover designer for pattern cut"
    # _rec_name = 'series_name'

    received_name = fields.Many2one('hr.employee', string="Receiver")
    received_date = fields.Date(string="Received Date")
    target_date = fields.Date(string="Target Date")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ], default='draft',
                             track_visibility='onchange')

    def update_pattern_cut_data(self):
        # this is for only form
        # self.env['merchandising.sheet.line'].browse(self._context.get("active_ids")).update({'received_name': self.received_name})
        # this is for line
        context = self.env.context
        active_ids = context.get('active_ids')
        for sale_rec in self.env['merchandising.sheet'].browse(active_ids):
            sale_rec.order_line = [(0, 0, {'received_name': self.received_name.name,
                                           'received_date': self.received_date,
                                           'target_date': self.target_date
                                           })]
        return True

    def pattern_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def pattern_cancel(self):
        for rec in self:
            rec.state = 'draft'

