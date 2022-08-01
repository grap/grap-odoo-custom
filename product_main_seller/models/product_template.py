# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    main_seller_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Main Seller Partner",
        help="Main Seller Partner of the product template",
        compute="_compute_main_seller_partner_id",
        store=True,
    )

    main_seller_variant_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Main Product Variant Seller Partner",
        help="Main Seller Partner of the product variant",
        related="product_variant_ids.product_main_seller_partner_id",
        store=True,
    )

    @api.multi
    @api.depends("seller_ids.sequence")
    def _compute_main_seller_partner_id(self):
        for product in self:
            if len(product.seller_ids):
                product.main_seller_partner_id = product.seller_ids[0].name
