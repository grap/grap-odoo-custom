# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    diff_product_main_first_seller = fields.Boolean(
        compute="_compute_diff_product_main_first_seller",
    )

    product_main_seller_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Main Product Seller Partner",
        help="Put your supplier info in first position to set as main supplier",
        compute="_compute_main_seller_partner_id",
        store=True,
    )

    @api.multi
    @api.depends("variant_seller_ids.sequence", "variant_seller_ids.name")
    def _compute_main_seller_partner_id(self):
        for prod in self:
            if len(prod.variant_seller_ids):
                prod.product_main_seller_partner_id = prod.variant_seller_ids[0].name

    # TEMP : In some case, main seller was not well calculated, and user
    # needs to set it by hand
    @api.multi
    def set_main_seller(self):
        self._compute_main_seller_partner_id()

    @api.multi
    @api.depends(
        "variant_seller_ids.sequence",
        "variant_seller_ids.name",
        "product_main_seller_partner_id",
    )
    def _compute_diff_product_main_first_seller(self):
        for prod in self:
            if len(prod.variant_seller_ids):
                if (
                    prod.product_main_seller_partner_id
                    != prod.variant_seller_ids[0].name
                ):
                    prod.diff_product_main_first_seller = True
                else:
                    prod.diff_product_main_first_seller = False
