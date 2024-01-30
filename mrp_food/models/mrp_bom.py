# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    image = fields.Binary(related="product_tmpl_id.image")
    image_2 = fields.Binary()
    image_3 = fields.Binary()

    @api.model
    def _get_bom_default_seasonalities(self):
        return self.env["seasonality"].search([("use_by_default_bom", "=", True)]).ids

    # Seasonality
    bom_season_ids = fields.Many2many(
        comodel_name="seasonality",
        string="Seasonality",
        help="Select the seasonality(s) of this Bill of material. "
        "Helps visually to know which recipe is in season or not.",
        default=lambda self: self._get_bom_default_seasonalities(),
    )
    is_bom_seasonal = fields.Boolean(
        string="Seasonal", default=False, compute="_compute_seasonal", store=True
    )
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
    def _is_bom_seasonal(self):
        self.ensure_one()
        # One Tag is in season, and we considere the BoM in season
        today = fields.Date.today()
        for period in self.mapped("bom_season_ids.seasonality_line_ids"):
            if period.date_start <= today <= period.date_end:
                return True
        return False

    @api.multi
    @api.depends("product_id", "bom_season_ids", "bom_line_ids")
    def _compute_seasonal(self):
        for bom in self:
            # Handling BoM Seasonalities
            # One Tag is in season, and we considere the BoM in season
            bom.is_bom_seasonal = bom._is_bom_seasonal()

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

    @api.model
    def cron_seasonality_bom_check_state(self):
        self.update_seasonality_value()

    @api.model
    def update_seasonality_value(self):
        all_boms = self.env["mrp.bom"].search([("bom_season_ids", "!=", False)])

        # Search values that will be updated
        boms_to_update = {}
        for bom in all_boms:
            new_is_seasonal = bom._is_bom_seasonal()
            if bom.is_bom_seasonal != new_is_seasonal:
                boms_to_update[bom.id] = {"is_bom_seasonal": new_is_seasonal}

        # Update all products in one write call
        if boms_to_update:
            for bom_id, values in boms_to_update.items():
                self.env["mrp.bom"].browse(bom_id).write(values)
