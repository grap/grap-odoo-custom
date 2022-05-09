# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # New fields
    standard_price_unit = fields.Float(related="product_id.standard_price")
    currency_id = fields.Many2one(related="product_id.currency_id")

    standard_price_subtotal = fields.Float(
        string="Subtotal price", compute="_compute_standard_price_subtotal"
    )

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
        comodel_name="mrp.seasonality",
        related="product_id.product_seasonality_ids",
        string="Seasonalities of the product",
    )

    @api.multi
    @api.depends("standard_price_unit", "product_qty")
    def _compute_standard_price_subtotal(self):
        for line in self:
            line.standard_price_subtotal = line.standard_price_unit * line.product_qty
