# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # Doing with Product and not product template
    product_tmpl_id = fields.Many2one(
        "product.template",
        "Product",
        related="product_id.product_tmpl_id",
        required=True,
    )

    product_id = fields.Many2one(
        "product.product",
        "Product Variant",
        domain="[('type', 'in', ['product', 'consu'])]",
        required=True,
    )

    currency_id = fields.Many2one(related="product_id.currency_id")

    image = fields.Binary(related="product_tmpl_id.image")

    bom_tag_ids = fields.Many2many(comodel_name="mrp.bom.tag", string="Tags")

    bom_season_ids = fields.Many2many(comodel_name="seasonality", string="Seasonality")

    is_bom_seasonal = fields.Boolean(default=False, compute="_compute_seasonal")
    are_bom_lines_seasonals = fields.Boolean(default=False, compute="_compute_seasonal")

    products_not_in_season = fields.Char(
        default="", compute="_compute_products_not_in_season"
    )

    bom_label_ids = fields.Many2many(
        comodel_name="product.label",
        string="Labels",
        help="BoM labels are not computed, you have to define them by hand",
    )

    bom_allergen_ids = fields.Many2many(
        comodel_name="product.allergen",
        string="Allergens",
        help="Includes allergens of the product and its components",
        compute="_compute_bom_allergen_ids",
        store=True,
    )

    standard_price_total = fields.Float(
        string="Cost", compute="_compute_standard_price_total"
    )

    # TODO : pourquoi pas déclencher au changement d'allergenes des lignes

    @api.multi
    @api.depends("product_id", "bom_line_ids.allergen_ids")
    def _compute_bom_allergen_ids(self):
        for bom in self:
            bom.bom_allergen_ids = bom.product_id.allergen_ids
            for bom_line in bom.bom_line_ids:
                bom.bom_allergen_ids = [x.id for x in bom_line.product_id.allergen_ids]

    @api.multi
    @api.depends("product_id", "bom_line_ids")
    def _compute_standard_price_total(self):
        for bom in self:
            # import pdb; pdb.set_trace()
            bom.standard_price_total = sum(
                x.standard_price_subtotal for x in bom.bom_line_ids
            )

    @api.multi
    @api.depends("product_id", "bom_line_ids")
    def _compute_seasonal(self):
        for bom in self:
            # Handling BoM Seasonalities
            # One Tag is in season, and we considere the BoM in season
            today = fields.Date.today()
            for seasonality in bom.bom_season_ids:
                for period in seasonality.seasonality_line_ids:
                    print("========== [BOM] DANS LA PERIODE " + str(period.name))
                    if today >= period.date_start and today <= period.date_end:
                        print("============ [BOM] De Saison grâce au tag")
                        bom.is_bom_seasonal = True
            #  Handling BoM Lines Seasonalities.
            #  One Line not in season and we considere the BoM Lines not in season
            bom.are_bom_lines_seasonals = True
            for bom_line in bom.bom_line_ids:
                if not bom_line.is_seasonal:
                    bom.are_bom_lines_seasonals = False
                    print("============ [BOM LINES] Pas de saison")

    @api.multi
    @api.depends("product_id", "bom_line_ids")
    def _compute_products_not_in_season(self):
        for bom in self:
            bom.products_not_in_season = ""
            for bom_line in bom.bom_line_ids.filtered(lambda x: x.is_seasonal is False):
                bom.products_not_in_season += str(bom_line.product_id.name) + ", "
            bom.products_not_in_season = bom.products_not_in_season[:-2] + "."
