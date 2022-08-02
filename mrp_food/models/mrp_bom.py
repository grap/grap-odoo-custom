# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    image = fields.Binary(related="product_tmpl_id.image")

    # Seasonality
    bom_season_ids = fields.Many2many(comodel_name="seasonality", string="Seasonality")
    is_bom_seasonal = fields.Boolean(default=False, compute="_compute_seasonal")
    are_bom_lines_seasonals = fields.Boolean(default=False, compute="_compute_seasonal")
    products_not_in_season = fields.Char(compute="_compute_products_not_in_season")

    # Labels, allergens
    bom_label_ids = fields.Many2many(
        comodel_name="product.label",
        string="Labels",
        help="BoM labels are not computed, you have to define them by hand",
    )

    bom_allergen_ids = fields.Many2many(
        string="Allergens",
        comodel_name="product.allergen",
        help="Includes allergens of the product and its components",
        compute="_compute_bom_allergen_ids",
        store=True,
    )

    #
    # Other functions
    #
    @api.multi
    @api.depends("product_id", "bom_line_ids.allergen_ids")
    def _compute_bom_allergen_ids(self):
        for bom in self:
            bom.bom_allergen_ids = bom.product_id.allergen_ids
            for bom_line in bom.bom_line_ids:
                bom.bom_allergen_ids = [x.id for x in bom_line.product_id.allergen_ids]

    @api.multi
    @api.depends("product_id", "bom_season_ids", "bom_line_ids")
    def _compute_seasonal(self):
        for bom in self:
            # Handling BoM Seasonalities
            # One Tag is in season, and we considere the BoM in season
            today = fields.Date.today()
            # for seasonality in bom.bom_season_ids:
            #     for period in seasonality.seasonality_line_ids:
            for period in bom.mapped("bom_season_ids.seasonality_line_ids"):
                if period.date_start <= today <= period.date_end:
                    bom.is_bom_seasonal = True
                    break
            #  Handling BoM Lines Seasonalities.
            #  One Line not in season and we considere the BoM Lines not in season
            bom.are_bom_lines_seasonals = True
            for bom_line in bom.bom_line_ids.filtered(
                lambda x: x.product_id.is_alimentary
            ):
                if not bom_line.is_seasonal:
                    bom.are_bom_lines_seasonals = False

    @api.multi
    @api.depends("product_id", "bom_line_ids")
    def _compute_products_not_in_season(self):
        for bom in self:
            bom.products_not_in_season = ""
            for bom_line in bom.bom_line_ids.filtered(
                lambda x: x.is_seasonal is False and x.product_id.is_alimentary is True
            ):
                bom.products_not_in_season += str(bom_line.product_id.name) + ", "
            bom.products_not_in_season = bom.products_not_in_season[:-2] + "."
