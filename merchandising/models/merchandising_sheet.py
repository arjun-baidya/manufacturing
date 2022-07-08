from odoo import fields, models, api, _


class MerchandisingSheet(models.Model):
    _name = 'merchandising.sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "merchandising sheet"
    _rec_name = 'reference'

    def get_manufacturing_order(self):
        data = self.env['mrp.production'].search([('md_sheet_id', '=', self.reference)])
        for rec in data:
            print('data', rec.name)

    reference = fields.Char('#MD NO', required=True, copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))
    customer_name = fields.Char(string="Customer Name")
    product = fields.Many2one('product.product', string="Product")
    series_name = fields.Char(string="Series Name")
    style_no = fields.Char(string="Style No")
    qty = fields.Integer(string="Quantity")
    brand_name = fields.Char(string="Brand Name")
    pattern_maker_name = fields.Many2one('hr.employee', string="Pattern Maker Name")
    sample_maker_name = fields.Many2one('hr.employee', string="Sample Maker Name")
    merchandiser_name = fields.Many2one('hr.employee', string="Merchandiser Maker Name")
    sample_lead_time = fields.Date(string="Sample Lead time")
    instruction = fields.Char(string="Instruction")
    manufacturing_order_no = fields.Many2one('mrp.production', string="Manufacturing order No ",)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('sample_document_register', 'Document Register'),
        ('bom', 'BOM'),
        ('sample_pattern_cut', 'Pattern Cut'),
        ('pattern_register', 'Pattern Register'),
        ('sample_cutting_skyving', 'Cutting Skyving'),
    ], default='draft', track_visibility='onchange')
    # link for sample.document.register model
    document_register_ids = fields.One2many('sample.document.register', 'merchandising_sheet_id',
                                            string='Document Register')
    order_line = fields.One2many('merchandising.sheet.line', 'order_id', string='Order Lines')
    pattern_cut_line_ids = fields.One2many('merchandising.sheet.line', 'order_id', string="Pattern Cut line")

    # link for mrp.bom model
    bom_ids = fields.One2many('mrp.bom', 'merchandising_sheet_id', string='BOM')

    # link for mrp.production model
    manufacturing_order_ids = fields.One2many('stock.move', 'merchandising_sheet_id', string='manufacturing order')

    # link for sample.pattern.cut model
    pattern_cut_ids = fields.One2many('sample.pattern.cut', 'merchandising_sheet_id',
                                      string='Pattern Cut')
    # link for pattern.register
    pattern_register_ids = fields.One2many('pattern.register', 'merchandising_sheet_id',
                                           string='Pattern register')
    # link for sample_cutting_skyving
    sample_cutting_skyving_ids = fields.One2many('sample.cutting.skyving', 'merchandising_sheet_id',
                                                 string='Pattern register')

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('merchandising.sheet.seq') or _('New')
        result = super(MerchandisingSheet, self).create(vals)
        return result

    @api.onchange('manufacturing_order_no')
    def onchange_qty(self):
        self.qty = self.manufacturing_order_no.product_qty

    def md_sheet_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    # go to sample.document.register model button
    def sample_document_register_load(self):
        for rec in self:
            rec.state = 'sample_document_register'
        # ref_obj = self.env['sample.document.register']
        # ref_obj.create(values)
        # so_id = self.env['sample.document.register'].search([('customer_name', '=', self.customer_name)]).id
        res = self.env.ref('merchandising.sample_document_register_form_view')
        result = {'name': _('Document Register'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'sample.document.register',
                  'context': {
                      'merchandising_sheet_id': self.id,
                  },
                  # 'res_id': self.id,
                  'type': 'ir.actions.act_window',
                  'target': 'current'}
        self.env['merchandising.sheet'].search([('id', '=', self.id)])
        return result

    # for bom
    def bom_load(self):
        for rec in self:
            rec.state = 'bom'
        res = self.env.ref('mrp.mrp_bom_form_view')
        result = {'name': _('bom'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'mrp.bom',
                  'context': {
                      'merchandising_sheet_id': self.id,
                  },
                  'type': 'ir.actions.act_window',
                  'target': 'current'}
        self.env['merchandising.sheet'].search([('id', '=', self.id)])
        return result

    # manufacturing order
    def manufacturing_order_load(self):
        for rec in self:
            rec.state = 'bom'
        res = self.env.ref('mrp.mrp_production_form_view')
        result = {'name': _('Manufacturing order'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'mrp.production',
                  'context': {
                      'merchandising_sheet_id': self.id,
                  },
                  'type': 'ir.actions.act_window',
                  'target': 'current'}
        self.env['merchandising.sheet'].search([('id', '=', self.id)])
        return result

    # go to sample.pattern.cut model button
    def sample_pattern_cut_load(self):
        for rec in self:
            rec.state = 'sample_pattern_cut'
        res = self.env.ref('merchandising.sample_pattern_cut_form_view')
        result = {'name': _('Pattern Cut'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'sample.pattern.cut',
                  'context': {
                      'merchandising_sheet_id': self.id,
                  },
                  # 'res_id': self.id,
                  'type': 'ir.actions.act_window',
                  'target': 'current'}
        self.env['merchandising.sheet'].search([('id', '=', self.id)])
        return result

    # go to pattern.register model button
    def sample_pattern_register_load(self):
        for rec in self:
            rec.state = 'pattern_register'
        res = self.env.ref('merchandising.pattern_register_form_view')
        result = {'name': _('Pattern Cut'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'pattern.register',
                  'context': {
                      'merchandising_sheet_id': self.id,
                  },
                  # 'res_id': self.id,
                  'type': 'ir.actions.act_window',
                  'target': 'current'}
        self.env['merchandising.sheet'].search([('id', '=', self.id)])
        return result

    # go to sample.cutting.skyving model button
    def sample_cutting_skyving_load(self):
        for rec in self:
            rec.state = 'sample_cutting_skyving'
        res = self.env.ref('merchandising.sample_cutting_skyving_form_view')
        result = {'name': _('Cutting Skyving'),
                  'view_type': 'form',
                  'view_mode': 'form',
                  'view_id': res and res.id or False,
                  'res_model': 'sample.cutting.skyving',
                  'context': {
                      'merchandising_sheet_id': self.id,
                  },
                  # 'res_id': self.id,
                  'type': 'ir.actions.act_window',
                  'target': 'current'}
        self.env['merchandising.sheet'].search([('id', '=', self.id)])
        return result


class MerchandisingSheetLine(models.Model):
    _name = 'merchandising.sheet.line'
    _description = 'Merchandising Sheet Line'
    _rec_name = 'part_name'

    product_category = fields.Many2one('product.category', string="Category")
    product_id = fields.Many2one('product.product', string='Material')
    pattern = fields.Many2one('sample.pattern.cut', string="Pattern")
    part_name = fields.Many2one('pattern.cut.line', string="Part Name")
    combination = fields.Many2many('product.product', string="Combination")
    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    pcs = fields.Integer(string="PCS")
    size = fields.Integer(string="Size")
    uom = fields.Many2one('uom.uom', string="UOM")
    net = fields.Float(string="Net", compute='calculate_net')
    factory_loss = fields.Float(string="Factory Loss %")
    buyer_loss = fields.Float(string="Buyer Loss %")
    purchase_loss = fields.Float(string="Purchase Loss %")
    net_loss = fields.Float(string="Net Loss", compute="calculate_net_loss", store=True)
    net_buyer = fields.Float(string="Net Buyer", compute='calculate_net_buyer', store=True)
    net_purchase = fields.Float(string="Net Purchase", compute='calculate_net_purchase')
    bom_no = fields.Many2one('mrp.bom', string="BOM")
    unit_price = fields.Float(string="Unit Price")
    total = fields.Float(string="Total")

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
            rec.factory_loss = rec.part_name.loss_percentage

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

    @api.depends('net', 'buyer_loss')
    def calculate_net_buyer(self):
        for rec in self:
            percentage = (rec.net * rec.buyer_loss) / 100
            rec.net_buyer = percentage + rec.net

    @api.depends('net', 'purchase_loss')
    def calculate_net_purchase(self):
        for rec in self:
            percentage = (rec.net * rec.purchase_loss) / 100
            rec.net_purchase = percentage + rec.net
