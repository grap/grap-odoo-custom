# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    product_categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Product Category",
        readonly=True,
        related="product_id.categ_id",
        store=True,
    )
