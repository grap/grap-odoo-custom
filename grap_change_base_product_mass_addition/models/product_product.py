# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    mass_addition_purchase_min_qty = fields.Float(
        compute="_compute_mass_addition_purchase",
    )

    mass_addition_purchase_multiplier_qty = fields.Float(
        compute="_compute_mass_addition_purchase",
    )

    mass_addition_purchase_price = fields.Float(
        compute="_compute_mass_addition_purchase",
    )

    mass_addition_purchase_discount = fields.Float(
        compute="_compute_mass_addition_purchase",
    )

    mass_addition_purchase_discount2 = fields.Float(
        compute="_compute_mass_addition_purchase",
    )

    mass_addition_purchase_min_qty_bad = fields.Boolean(
        compute="_compute_mass_addition_purchase_bad",
    )

    mass_addition_purchase_multiplier_qty_bad = fields.Boolean(
        compute="_compute_mass_addition_purchase_bad",
    )

    @api.depends(
        "qty_to_process",
        "mass_addition_purchase_min_qty",
        "mass_addition_purchase_multiplier_qty",
    )
    def _compute_mass_addition_purchase_bad(self):
        for product in self:
            product.mass_addition_purchase_min_qty_bad = False
            product.mass_addition_purchase_multiplier_qty_bad = False

            if product.qty_to_process and product.mass_addition_purchase_min_qty:
                product.mass_addition_purchase_min_qty_bad = (
                    product.qty_to_process < product.mass_addition_purchase_min_qty
                )

            if product.qty_to_process and product.mass_addition_purchase_multiplier_qty:
                product.mass_addition_purchase_multiplier_qty_bad = (
                    product.qty_to_process
                    % product.mass_addition_purchase_multiplier_qty
                )

    def _compute_mass_addition_purchase(self):
        PurchaseOrder = self.env["purchase.order"]

        for product in self:
            product.mass_addition_purchase_min_qty = 0
            product.mass_addition_purchase_multiplier_qty = 0
            product.mass_addition_purchase_price = 0
            product.mass_addition_purchase_discount = 0
            product.mass_addition_purchase_discount2 = 0

        if self.env.context.get("parent_model") != "purchase.order":
            return

        order = PurchaseOrder.browse(self.env.context.get("parent_id"))

        for product in self.filtered(lambda x: x.id):
            sellers = product.seller_ids.filtered(
                lambda r: r.partner_id == order.partner_id
            ).sorted(key=lambda r: r.min_qty)

            if sellers:
                seller = sellers[0]
                product.mass_addition_purchase_min_qty = seller.min_qty
                product.mass_addition_purchase_multiplier_qty = seller.multiplier_qty
                product.mass_addition_purchase_price = seller.price
                product.mass_addition_purchase_discount = seller.discount
                product.mass_addition_purchase_discount2 = seller.discount2
