from odoo import fields, models, api, _


class ProductCategoryFilter(models.Model):
    _inherit = 'product.category'
    _parent_name = "parent_id"

    parent_id = fields.Many2one('product.category', 'parent id', index=True, ondelete='cascade')

    def _generate_categories(self, categories, product_category):
        categories.append(product_category)
        for cat in self.search([('parent_id', '=', product_category)]):
            categories = self._generate_categories(categories, cat.id)
        return categories

    def get_categories(self, product_category):
        categories = []
        categories = self._generate_categories(categories, product_category)
        return categories

