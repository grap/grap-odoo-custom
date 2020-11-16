# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    mass_addition_purchase_min_qty = fields.Float(
        compute='_compute_mass_addition_purchase',
    )

    mass_addition_purchase_package_qty = fields.Float(
        compute='_compute_mass_addition_purchase',
    )

    mass_addition_purchase_price = fields.Float(
        compute='_compute_mass_addition_purchase',
    )

    mass_addition_purchase_discount = fields.Float(
        compute='_compute_mass_addition_purchase',
    )

    mass_addition_purchase_discount2 = fields.Float(
        compute='_compute_mass_addition_purchase',
    )

    mass_addition_purchase_min_qty_bad = fields.Boolean(
        compute='_compute_mass_addition_purchase_bad',
    )

    mass_addition_purchase_package_qty_bad = fields.Boolean(
        compute='_compute_mass_addition_purchase_bad',
    )

    @api.multi
    @api.depends(
        "qty_to_process", "mass_addition_purchase_min_qty",
        "mass_addition_purchase_package_qty")
    def _compute_mass_addition_purchase_bad(self):
        for product in self.filtered(
                lambda x: x.qty_to_process and
                x.mass_addition_purchase_min_qty):
            product.mass_addition_purchase_min_qty_bad =\
                product.qty_to_process < product.mass_addition_purchase_min_qty
        for product in self.filtered(
                lambda x: x.qty_to_process and
                x.mass_addition_purchase_package_qty):
            product.mass_addition_purchase_package_qty_bad =\
                product.qty_to_process %\
                product.mass_addition_purchase_package_qty

    @api.multi
    def _compute_mass_addition_purchase(self):
        PurchaseOrder = self.env["purchase.order"]
        if self.env.context.get("parent_model", False) == "purchase.order":
            order = PurchaseOrder.browse(
                [self.env.context.get("parent_id")])[0]

        for product in self.filtered(lambda x: x.id):
            sellers = product.seller_ids\
                .filtered(lambda r: r.name == order.partner_id)\
                .sorted(key=lambda r: r.min_qty)

            if sellers:
                product.mass_addition_purchase_min_qty = sellers[0].min_qty
                product.mass_addition_purchase_package_qty =\
                    sellers[0].package_qty
                product.mass_addition_purchase_price = sellers[0].price
                product.mass_addition_purchase_discount = sellers[0].discount
                product.mass_addition_purchase_discount2 = sellers[0].discount2

    def _inverse_set_process_qty(self):
        parent_model = self.env.context.get('parent_model')
        parent_id = self.env.context.get('parent_id')
        PurchaseOrderLine = self.env["purchase.order.line"]
        if parent_model == "purchase.order":
            order = self.env[parent_model].browse(parent_id)
            for product in self:
                # we conserve the value because the call
                # of play_onchanges reset the value. That's the magic !
                new_qty = product.qty_to_process
                order_line = order._get_quick_line(product)
                if order_line:
                    if new_qty:
                        # Update mode
                        order_line.product_qty = product.qty_to_process
                    else:
                        pass
                        order_line.unlink()
                else:
                    # Create Mode
                    vals = {
                        "order_id": parent_id,
                        "product_id": product.id,
                        "product_qty": new_qty,
                    }
                    vals = PurchaseOrderLine.play_onchanges(
                        vals, ["product_id", "product_qty"])
                    # We pop product_image, to avoid a useless write
                    # to ir.attachment
                    if 'product_image' in vals.keys():
                        vals.pop('product_image')
                    PurchaseOrderLine.create(
                        PurchaseOrderLine._convert_to_write(vals)
                    )
        else:
            return super()._inverse_set_process_qty()
