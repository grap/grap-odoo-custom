# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    date_last_statement_price = fields.Date(
        string="Date Last Statement Price",
        help="Date of last standard price change. "
        "Automatically sets to the date of the day you changed the standard price",
    )
    end_date_of_market_price_list = fields.Date(
        string="End Date of Market Price List",
        help="End date of validity of the market price list. "
        "After this date, you can consider that your standard price is "
        "certainly not up to date.",
    )

    @api.model
    def _get_default_seasonalities(self):
        return (
            self.env["seasonality"].search([("use_by_default_product", "=", True)]).ids
        )

    product_seasonality_ids = fields.Many2many(
        comodel_name="seasonality",
        string="Seasonalities",
        default=lambda self: self._get_default_seasonalities(),
    )

    is_seasonal = fields.Boolean(
        string="Is Seasonal",
        help="Computed thanks to choosen seasonalities.\
              It is enough that a selected season matches",
        compute="_compute_is_seasonal",
        default=False,
    )
    # because the computation is based on mrp.bom.line,
    # that is not available for user that doesn't belong to mrp user group
    is_component = fields.Boolean(
        compute="_compute_is_component_intermediate",
        compute_sudo=True,
        store=True,
        help="Is component a product which has no BoM based on it +\
              not to sale + is used in a BoM line",
    )
    is_intermediate = fields.Boolean(
        string="Intermediate product",
        compute="_compute_is_component_intermediate",
        compute_sudo=True,
        store=True,
        help="Is intermediate a product which has a BoM based on it +\
              is or is not to sale + is used in a BoM line",
    )

    @api.onchange("standard_price")
    def _onchange_date_last_statement_price(self):
        for product in self:
            product.date_last_statement_price = fields.Date.today()

    @api.multi
    def _compute_is_seasonal(self):
        today = fields.Date.today()
        for product in self:
            for seasonality in product.product_seasonality_ids:
                for period in seasonality.seasonality_line_ids:
                    if today >= period.date_start and today <= period.date_end:
                        product.is_seasonal = True

    @api.depends("bom_line_ids")
    @api.multi
    def _compute_is_component_intermediate(self):
        for product in self:
            if product.bom_line_ids:
                # Difference is having a BoM with this product or not
                product.is_intermediate = True if product.bom_count else False
                product.is_component = not product.is_intermediate
            else:
                product.is_intermediate = False
                product.is_component = False
