# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    date_last_statement_price = fields.Date(string="Date Last Statement Price")

    product_seasonality_ids = fields.Many2many(
        comodel_name="seasonality", string="Seasonality"
    )

    is_seasonal = fields.Boolean(
        string="Seasonal",
        help="Computed thanks to choosen seasonalities. It is enough that a selected season matches",
        compute="_compute_is_seasonal",
        default=False,
    )

    main_seller_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Main Seller Partner",
        help="Main Seller Partner of the product",
        compute="_compute_main_seller_partner_id",
        store=True,
    )

    @api.multi
    @api.depends("variant_seller_ids.sequence")
    def _compute_main_seller_partner_id(self):
        for product in self:
            if len(product.variant_seller_ids):
                product.main_seller_partner_id = product.variant_seller_ids[0].name

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
                    print("========== [PRODUCT] DANS LA PERIODE " + str(period.name))
                    if today >= period.date_start and today <= period.date_end:
                        product.is_seasonal = True

    # @api.multi
    # def _compute_is_seasonal(self):
    #     today = fields.Date.today()
    #     for product in self:
    #         for period in product.filtered(lambda x: x.product_seasonality_ids.seasonality_line_ids):
    #             print("========== DANS LA PERIODE " + str(period.name))
    #             if today >= period.date_start and today <= period.date_end:
    #                 product.is_seasonal = True
