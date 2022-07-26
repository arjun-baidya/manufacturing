from odoo import fields, models, api, _
import datetime


class MerchandisingSheet(models.Model):
    _name = 'merchandising.sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _inherits = {'sample.pattern.cut': 'pattern_cut'}
    _description = "merchandising sheet"
    _rec_name = 'reference'

    # pattern_cut = fields.Many2one('sample.pattern.cut', "Source", ondelete='cascade', required=True)
    reference = fields.Char('#MD NO', required=True, copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))
    customer_name = fields.Many2one('res.partner', string="Customer")
    product = fields.Many2one('product.product', string="Product")
    series_name = fields.Char(string="Series")
    style_no = fields.Char(string="Style")
    images = fields.Image(string="Image", max_width=120, max_height=120)
    # qty = fields.Integer(string="Quantity")
    brand_name = fields.Char(string="Brand")
    pattern_maker_name = fields.Many2one('hr.employee', string="Pattern Maker")
    sample_maker_name = fields.Many2one('hr.employee', string="Sample Maker")
    merchandiser_name = fields.Many2one('hr.employee', string="Merchandiser")
    sample_lead_time = fields.Date(string="Sample Lead time")
    # manufacturing_order_no = fields.Many2one('mrp.production', string="Manufacturing order No ", )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('sample_document_register', 'Document Register'),
        ('bom', 'BOM'),
        ('sample_pattern_cut', 'Pattern Cut'),
        ('pattern_register', 'Pattern Register'),
        ('sample_cutting_skyving', 'Cutting Skyving'),
    ], default='draft', track_visibility='onchange')

    order_line = fields.One2many('merchandising.sheet.line', 'order_id', string='Order Lines')
    consumption_line_ids = fields.One2many('consumption.line',
                                           'consumption_line_id', string="ids")
    pattern_cut_line_ids = fields.One2many('merchandising.sheet.line', 'order_id', string="Pattern Cut line")
    instruction_line_ids = fields.One2many('instruction.line', 'instruction_line_id', string="ids")
    # link for sample.pattern.cut model
    pattern_cut_ids = fields.One2many('sample.pattern.cut', 'merchandising_sheet_id',
                                      string='Pattern Cut')

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('merchandising.sheet.seq') or _('New')
        result = super(MerchandisingSheet, self).create(vals)
        return result

    # @api.onchange('manufacturing_order_no')
    # def onchange_qty(self):
    #     self.qty = self.manufacturing_order_no.product_qty

    def md_sheet_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    # def merge_duplicate_materials(self):
    #     if self.order_line:
    #         for line in self.order_line:
    #             if line.id in self.order_line.ids:
    #                 line_ids = self.order_line.filtered(lambda m: m.product_id.id == line.product_id.id)
    #                 net_for_report = 0.0
    #                 total_for_report = 0.0
    #                 for qty in line_ids:
    #                     net_for_report += qty.net
    #                     total_for_report += qty.total
    #                 line_ids[0].write({
    #                     'product_id_for_report': line_ids[0].product_id.name,
    #                     'net_for_report': net_for_report,
    #                     'uom_for_report': line_ids[0].uom.name,
    #                     'net_loss_for_report': line_ids[0].net_loss,
    #                     'unit_price_for_report': line_ids[0].unit_price,
    #                     'total_for_report': total_for_report,
    #                 })
    #                 # line_ids[1:].unlink()

    def merge_duplicate_materials(self):
        if self.order_line:
            lines = [(5, 0, 0)]
            for line in self.order_line:
                if line.id in self.order_line.ids:
                    line_ids = self.order_line.filtered(lambda m: m.product_id.id == line.product_id.id)
                    net_for_report = 0.0
                    # total_for_report = 0.0
                    for qty in line_ids:
                        net_for_report += qty.net
                        # total_for_report += qty.total
                    val = {
                        'product_id_for_report': line_ids[0].product_id.name,
                        'net_for_report': net_for_report,
                        'uom_for_report': line_ids[0].uom.name,
                        # 'net_loss_for_report': line_ids[0].net_loss,
                        # 'unit_price_for_report': line_ids[0].unit_price,
                        # 'total_for_report': total_for_report,
                        'arrange_by': '',
                        'supplier': '',
                    }
                lines.append((0, 0, val))
                self.consumption_line_ids = lines
                self.merge_consumption_line()

    def merge_consumption_line(self):
        if self.consumption_line_ids:
            for line in self.consumption_line_ids:
                if line.id in self.consumption_line_ids.ids:
                    line_ids = self.consumption_line_ids.filtered(
                        lambda m: m.product_id_for_report == line.product_id_for_report)
                    line_ids[0].write({
                        'product_id_for_report': line_ids[0].product_id_for_report,
                    })
                    line_ids[1:].unlink()


class MerchandisingSheetLine(models.Model):
    _name = 'merchandising.sheet.line'
    _description = 'Merchandising Sheet Line'
    _rec_name = 'part_name'

    product_category = fields.Many2one('product.category', string="Category")
    product_id = fields.Many2one('product.product', string='Material')
    product_id_for_report = fields.Char()
    pattern = fields.Many2one('sample.pattern.cut', string="Pattern")
    part_name = fields.Many2one('pattern.cut.line', string="Part Name")
    type = fields.Selection(
        [('leather', 'Leather'), ('lining', 'Lining'), ('rf', 'Reinforcement'), ('zipper', 'Zipper')], required=True)
    combination = fields.Many2many('product.product', string="Combination")
    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    pcs = fields.Integer(string="PCS")
    consumption = fields.Float(string="Consumption", compute="compute_calc")
    size = fields.Integer(string="Size")
    uom = fields.Many2one('uom.uom', string="UOM")
    uom_for_report = fields.Char()
    net = fields.Float(string="Net", compute='calculate_net')
    net_for_report = fields.Float()
    factory_loss = fields.Float(string="Factory Loss %")
    net_loss = fields.Float(string="Net Loss", compute="calculate_net_loss", store=True)
    net_loss_for_report = fields.Float()
    # unit_price = fields.Float(string="Unit Price")
    # unit_price_for_report = fields.Float()
    # total = fields.Float(string="Total")
    # total_for_report = fields.Float()

    ##################
    order_id = fields.Many2one('merchandising.sheet', string='Order Reference')

    # part name filter material wise
    @api.onchange('pattern')
    def onchange_category(self):
        res = {}
        self.part_name = 0
        ids = []
        category = self.env['sample.pattern.cut'].get_categories(self.pattern.id)
        templates = self.env['pattern.cut.line'].search([('patten_cut_id', 'in', category)])
        for record in templates:
            ids.append(record.id)
        res['domain'] = {
            'part_name': [('id', 'in', ids)]
        }
        return res

    # product filter category wise
    @api.onchange('product_category')
    def onchange_product_category(self):
        res = {}
        self.product_id = 0
        ids = []
        category = self.env['product.category'].get_categories(self.product_category.id)
        templates = self.env['product.template'].search([('categ_id', 'in', category)])
        for record in templates:
            ids.append(record.id)
        res['domain'] = {
            'product_id': [('id', 'in', ids)]
        }
        return res

    @api.onchange('part_name')
    def onchange_data(self):
        for rec in self:
            rec.length = rec.part_name.length
            rec.width = rec.part_name.width
            rec.pcs = rec.part_name.pcs
            rec.size = rec.part_name.size
            rec.uom = rec.part_name.uom
            # rec.factory_loss = rec.part_name.loss_percentage

    @api.depends('length', 'width', 'pcs')
    def calculate_net(self):
        for rec in self:
            rec_net = (rec.length * rec.width * rec.pcs)
            rec.net = rec_net / 929

    @api.depends('net', 'factory_loss')
    def calculate_net_loss(self):
        for rec in self:
            percentage = (rec.net * rec.factory_loss) / 100
            rec.net_loss = percentage + rec.net

    @api.depends('length', 'width', 'pcs')
    def compute_calc(self):
        for rec in self:
            rec.consumption = rec.length * rec.width * rec.pcs


class ConsumptionLine(models.Model):
    _name = 'consumption.line'
    _description = "consumption line"

    product_id_for_report = fields.Char(string="Materials")
    uom_for_report = fields.Char(string="UOM")
    net_for_report = fields.Float(string="Net")
    # net_loss_for_report = fields.Float(string="Net Loss")
    buyer_loss = fields.Float(string="Buyer Loss %")
    purchase_loss = fields.Float(string="Purchase Loss %")
    net_buyer = fields.Float(string="Net Buyer", compute='calculate_net_buyer', store=True)
    net_purchase = fields.Float(string="Net Purchase", compute='calculate_net_purchase')
    bom_no = fields.Many2one('mrp.bom', string="BOM")
    unit_price_for_report = fields.Float(string="Unit Price")
    total_for_report = fields.Float(string="Total")
    arrange_by = fields.Many2one('res.partner', string="Arrange-By")
    supplier = fields.Many2one('res.partner', string="Supplier", help="Maker")
    consumption_line_id = fields.Many2one('merchandising.sheet', string="id")

    @api.depends('net_for_report', 'buyer_loss')
    def calculate_net_buyer(self):
        for rec in self:
            percentage = (rec.net_for_report * rec.buyer_loss) / 100
            rec.net_buyer = percentage + rec.net_for_report

    @api.depends('net_for_report', 'purchase_loss')
    def calculate_net_purchase(self):
        for rec in self:
            percentage = (rec.net_for_report * rec.purchase_loss) / 100
            rec.net_purchase = percentage + rec.net_for_report


class InstructionLine(models.Model):
    _name = 'instruction.line'
    _description = "Instruction Line model"

    instruction_name = fields.Char(string="Name")
    date = fields.Datetime('Last Poll', default=lambda self: fields.Datetime.now())
    attachment = fields.Binary(string="Attachment")
    instruction_line_id = fields.Many2one('merchandising.sheet', string="id")



