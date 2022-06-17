# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    currency_id = fields.Many2one(related="product_id.currency_id")

    image = fields.Binary(related="product_tmpl_id.image")

    # override product_uom_id to make it related to product uom
    product_uom_id = fields.Many2one(
        "uom.uom",
        "Product Unit of Measure",
        related="product_id.uom_id",
        oldname="product_uom",
        required=True,
    )

    standard_price_total = fields.Float(
        string="Cost", compute="_compute_standard_price_total"
    )

    code = fields.Char(
        compute="_compute_proposal_code",
        inverse="_inverse_proposal_code",
        store=True,
    )
    _BOM_CODE_SEQ_START = _("FT")

    # Models methods
    @api.multi
    def _get_bom_code_start(self):
        self.ensure_one()
        if not self.product_id:
            return 0
        else:
            product_name_start = self.product_id.name[0:3].upper()
            bom_code = self._BOM_CODE_SEQ_START
            if self.env.user.company_id.code:
                bom_code += ("-") + self.env.user.company_id.code
            bom_code += ("-") + product_name_start
            return bom_code

    # Override function
    # We have to override copy function, otherwise, when we duplicate BoM
    # the bom_count of the product is not accurate (it counts the one being created)
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        if self.product_id:
            count = self.product_id.bom_count
        new_code = self._get_bom_code_start() + ("-") + str(count + 1)
        default.update(
            {
                "code": new_code,
            }
        )
        return super(MrpBom, self).copy(default)

    # BoM code
    @api.depends("product_id")
    def _compute_proposal_code(self):
        for bom in self:
            if bom.product_id:
                bom.code = self._get_bom_code_start()
                bom.code += ("-") + str(self.product_id.bom_count + 1)

    def _inverse_proposal_code(self):
        return True

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

    # TODO : Handling time

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
            bom.standard_price_total = sum(
                x.standard_price_subtotal for x in bom.bom_line_ids
            )

    @api.multi
    @api.depends("product_id", "bom_season_ids", "bom_line_ids")
    def _compute_seasonal(self):
        for bom in self:
            # Handling BoM Seasonalities
            # One Tag is in season, and we considere the BoM in season
            today = fields.Date.today()
            for seasonality in bom.bom_season_ids:
                for period in seasonality.seasonality_line_ids:
                    if period.date_start <= today <= period.date_end:
                        bom.is_bom_seasonal = True
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