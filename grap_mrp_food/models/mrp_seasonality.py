# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpSeasonality(models.Model):
    _name = "mrp.seasonality"
    _description = "MRP Seasonality"

    # Column Section
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda s: s._default_company_id(),
    )

    name = fields.Char(string="Seasonality name", required=True)

    color = fields.Integer("Color Index", default=0)

    bom_ids = fields.Many2many(
        comodel_name="mrp.bom",
        inverse_name="bom_season_ids",
    )

    bom_qty = fields.Integer(
        string="BoM Quantity", compute="_compute_bom_qty", store=True
    )

    product_product_ids = fields.Many2many(
        comodel_name="product.product",
        inverse_name="product_seasonality_ids",
    )

    product_product_qty = fields.Integer(
        string="Product Variant Quantity",
        compute="_compute_product_product_qty",
        store=True,
    )

    @api.depends("bom_ids")
    def _compute_bom_qty(self):
        for seasonality in self:
            seasonality.bom_qty = len(seasonality.bom_ids)

    @api.depends("product_product_ids")
    def _compute_product_product_qty(self):
        for seasonality in self:
            seasonality.product_product_qty = len(seasonality.product_product_ids)

    # Default Section
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id
