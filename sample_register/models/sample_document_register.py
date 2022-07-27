from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class SampleDocumentRegister(models.Model):
    _name = 'sample.document.register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Sample Document register model"
    _rec_name = 'name'

    name = fields.Char('#SL NO', required=True, copy=False, readonly=True, index=True,
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
    sample_document_line_ids = fields.One2many('sample.document.register.line', 'sample_document_line_id', string="ids")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('document.register.sequence') or _('New')
        result = super(SampleDocumentRegister, self).create(vals)
        return result

    def document_save(self):
        for rec in self:
            rec.state = 'confirm'

    def document_cancel(self):
        for rec in self:
            rec.state = 'draft'

    def unlink(self):
        for a in self:
            if a.state != 'draft':
                raise UserError(_('You can not delete this.'))
            return super(SampleDocumentRegister, self).unlink()


class SampleDocumentRegisterLine(models.Model):
    _name = 'sample.document.register.line'
    _description = "sample document register line model"

    issued_date = fields.Date(string="Issued Date")
    issued_to = fields.Char(string="Issued To")
    issued_by = fields.Char(string="Issued By")
    return_date = fields.Date(string="Return Date")
    return_received_by = fields.Char(string="Return received By")
    sample_document_line_id = fields.Many2one('sample.document.register', string="Document")
