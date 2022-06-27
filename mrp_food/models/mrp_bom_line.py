# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # New fields
    label_ids = fields.Many2many(
        comodel_name="product.label",
        related="product_id.label_ids",
        string="Labels on product",
    )

    allergen_ids = fields.Many2many(
        comodel_name="product.allergen",
        related="product_id.allergen_ids",
        string="Allergens on product",
    )

    seasonality_ids = fields.Many2many(
        comodel_name="seasonality",
        related="product_id.product_seasonality_ids",
        string="Seasonalities of the product",
    )

    is_seasonal = fields.Boolean(
        related="product_id.is_seasonal",
    )
