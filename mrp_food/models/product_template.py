# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    date_last_statement_price = fields.Date(
        string="Date Last Statement Price",
        related="product_variant_ids.date_last_statement_price",
        readonly=False,
    )

    product_seasonality_ids = fields.Many2many(
        comodel_name="seasonality",
        string="Seasonalities",
        related="product_variant_ids.product_seasonality_ids",
        readonly=False,
    )

    is_seasonal = fields.Boolean(
        string="Is Seasonal",
        help="Computed thanks to choosen seasonalities.\
              It is enough that a selected season matches",
        related="product_variant_ids.is_seasonal",
        default=False,
        readonly=False,
    )

    is_component = fields.Boolean(
        related="product_variant_ids.is_component", default=False, readonly=False
    )
