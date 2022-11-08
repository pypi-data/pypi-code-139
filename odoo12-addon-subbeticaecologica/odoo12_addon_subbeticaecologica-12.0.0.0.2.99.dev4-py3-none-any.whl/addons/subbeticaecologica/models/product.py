from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_published = fields.Boolean(
        'Visible on current website',
        compute='_compute_unpublish_product_without_availability'
    )

    @api.depends('inventory_availability','virtual_available')
    def _compute_unpublish_product_without_availability(self):
        for record in self:
            if record.inventory_availability == 'always' and record.virtual_available == 0:
                record.is_published = False
            else:
                record.is_published = True
