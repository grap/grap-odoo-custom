# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    mass_addition_purchase_min_qty = fields.Float(
        compute="_compute_mass_addition_purchase"
    )

    mass_addition_purchase_multiplier_qty = fields.Float(
        compute="_compute_mass_addition_purchase"
    )

    mass_addition_purchase_discount1 = fields.Float(
        compute="_compute_mass_addition_purchase"
    )

    mass_addition_purchase_discount2 = fields.Float(
        compute="_compute_mass_addition_purchase"
    )

    mass_addition_purchase_min_qty_bad = fields.Boolean(
        compute="_compute_mass_addition_purchase_bad"
    )

    mass_addition_purchase_multiplier_qty_bad = fields.Boolean(
        compute="_compute_mass_addition_purchase_bad"
    )

    @api.depends(
        "qty_to_process",
        "mass_addition_purchase_min_qty",
        "mass_addition_purchase_multiplier_qty",
    )
    def _compute_mass_addition_purchase_bad(self):
        for product in self.filtered(lambda x: not x.qty_to_process):
            product.mass_addition_purchase_min_qty_bad = False
            product.mass_addition_purchase_multiplier_qty_bad = False

        for product in self.filtered(lambda x: x.qty_to_process):
            product.mass_addition_purchase_min_qty_bad = (
                product.mass_addition_purchase_min_qty
                and (product.qty_to_process < product.mass_addition_purchase_min_qty)
            )
            product.mass_addition_purchase_multiplier_qty_bad = (
                product.mass_addition_purchase_multiplier_qty
                and (
                    product.qty_to_process
                    % product.mass_addition_purchase_multiplier_qty
                )
            )

    def _compute_mass_addition_purchase(self):
        po = self.pma_parent
        for product in self:
            seller = product.seller_ids.filtered(
                lambda r: r.partner_id == po.partner_id
            ).sorted(key=lambda r: r.min_qty)[0]
            product.mass_addition_purchase_min_qty = seller.min_qty
            product.mass_addition_purchase_multiplier_qty = seller.multiplier_qty
            product.mass_addition_purchase_discount1 = seller.discount1
            product.mass_addition_purchase_discount2 = seller.discount2
