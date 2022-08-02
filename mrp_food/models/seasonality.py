# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class Seasonality(models.Model):
    _name = "seasonality"
    _description = "Seasonality"

    # Column Section
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda s: s._default_company_id(),
    )

    name = fields.Char(string="Seasonality name", required=True)
    color = fields.Integer("Color Index", default=0)

    seasonality_line_ids = fields.One2many(
        comodel_name="seasonality.line",
        inverse_name="seasonality_id",
        string="Seasonality lines",
    )

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

    # Compute methods
    @api.depends("bom_ids")
    def _compute_bom_qty(self):
        for seasonality in self:
            seasonality.bom_qty = len(seasonality.bom_ids)

    @api.depends("product_product_ids")
    def _compute_product_product_qty(self):
        for seasonality in self:
            seasonality.product_product_qty = len(seasonality.product_product_ids)

    # Default methos
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    # Action methods
    @api.multi
    def add_seasonality_line_one_more_year(self):
        for seasonality in self:
            if not len(seasonality.seasonality_line_ids):
                raise AccessError(
                    _(
                        "You cannot use this button. "
                        "Fill one period for this seasonality before."
                    )
                )
            last_seasonality_line = seasonality.seasonality_line_ids[-1]

            new_date_start = last_seasonality_line.date_start + relativedelta(years=1)
            new_date_end = last_seasonality_line.date_end + relativedelta(years=1)
            new_name = self._compute_name_with_one_year_more(
                last_seasonality_line.name, new_date_start.year
            )
            seasonality.seasonality_line_ids = [
                (
                    0,
                    0,
                    {
                        "name": new_name,
                        "date_start": new_date_start,
                        "date_end": new_date_end,
                    },
                )
            ]

    def _compute_name_with_one_year_more(self, name, year):
        # Clean name of potential year created by human then by this method
        clean_name = re.sub("[0-9]*", "", name)
        clean_name = re.sub(r"\([0-9]*\)", "", clean_name)

        new_name = clean_name + "(" + str(year) + ")"
        return new_name
