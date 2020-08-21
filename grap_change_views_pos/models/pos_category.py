# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PosCategory(models.Model):
    _inherit = "pos.category"

    # Columns Section
    product_ids = fields.One2many(
        comodel_name="product.product",
        inverse_name="pos_categ_id",
        string="Products",
        readonly=True,
    )

    product_qty = fields.Integer(
        string="Product Qty",
        compute="_compute_product_qty",
        store=True,
    )

    # Compute Section
    @api.depends("product_ids.pos_categ_id")
    def _compute_product_qty(self):
        product_obj = self.env['product.product']
        for category in self:
            products = product_obj.search_count([
                '&', ('pos_categ_id', '=', category.id),
                ('active', '=', True)
            ])
            category.product_qty = products
