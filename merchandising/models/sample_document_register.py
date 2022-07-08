from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class SampleDocumentRegister(models.Model):
    _name = 'sample.document.register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Sample Document register model"
    _rec_name = 'serial_num'

    serial_num = fields.Char('#SL NO', required=True, copy=False, readonly=True, index=True,
                             default=lambda self: _('New'))
    customer_name = fields.Char(string="Customer Name")
    style_no = fields.Char(string="Style No")
    series_name = fields.Char(string="Series Name")
    color = fields.Char(string="Color")
    register_date = fields.Date(string="Register Date")
    quantity = fields.Integer(string="Quantity")
    document_type = fields.Selection([('returnable', 'Returnable'), ('nonreturnable', 'Non-Returnable')],
                                     string="Document Type")
    receiver_name = fields.Many2one('hr.employee', string="Receiver Name")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ], default='draft',
                             track_visibility='onchange')
    sample_document_register_line = fields.One2many('sample.document.register.line', 'document_ids', string="document "
                                                                                                            "register"
                                                                                                            " line")
    merchandising_sheet_id = fields.Many2one("merchandising.sheet", string='Merchandising Sheet', ondelete='cascade',
                                             readonly=True,
                                             default=lambda self: self.env.context.get('merchandising_sheet_id'))
    mds_ids = fields.Many2many('merchandising.sheet', 'mds_document_rel', 'md_id', 'document_id', string='MD No')

    @api.model
    def create(self, vals):
        if vals.get('serial_num', _('New')) == _('New'):
            vals['serial_num'] = self.env['ir.sequence'].next_by_code('sample.document.register.sequence') or _('New')
        result = super(SampleDocumentRegister, self).create(vals)
        return result

    # onChange for value pass from md sheet
    @api.onchange('mds_ids')
    def onchange_md(self):
        self.customer_name = self.mds_ids.customer_name
        self.series_name = self.mds_ids.series_name
        self.style_no = self.mds_ids.style_no

    def document_save(self):
        for rec in self:
            rec.state = 'confirm'

    def document_cancel(self):
        for rec in self:
            rec.state = 'draft'

    def action_view_document_register(self):

        res = self.env.ref('merchandising.sample_document_register_form_view')

        result = {'name': _('Document Register'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'sample.document.register',
                  'type': 'ir.actions.act_window',
                  'target': 'current',
                  'res_id': self.id}
        return result

    def unlink(self):
        for a in self:
            if a.state != 'draft':
                raise UserError(_('You can not delete this.'))
            return super(SampleDocumentRegister, self).unlink()


class SampleDocumentRegisterLine(models.Model):
    _name = 'sample.document.register.line'
    _description = "sample document register line model"

    document_ids = fields.Many2one('sample.document.register', string="Document")
    issued_date = fields.Date(string="Issued Date")
    issued_to = fields.Char(string="Issued To")
    issued_by = fields.Char(string="Issued By")
    return_date = fields.Date(string="Return Date")
    return_received_by = fields.Char(string="Return received By")
