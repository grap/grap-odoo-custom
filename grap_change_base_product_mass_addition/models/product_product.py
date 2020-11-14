# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _inverse_set_process_qty(self):
        parent_model = self.env.context.get('parent_model')
        parent_id = self.env.context.get('parent_id')
        if parent_model == "purchase.order":
            order = self.env[parent_model].browse(parent_id)
            for product in self:
                order_line = order._get_quick_line(product)
                if order_line:
                    order_line.product_qty = product.qty_to_process
                    order_line._onchange_quantity()
                else:
                    order_line = self.env["purchase.order.line"].new({
                        "order_id": parent_id,
                        "product_id": product.id,
                        })
                    order_line.onchange_product_id()
                    order_line.name = order_line.product_id.with_context(
                        lang=order_line.order_id.partner_id.lang,
                        partner_id=order_line.order_id.partner_id.id,
                    ).display_name
                    order_line.product_qty = product.qty_to_process
                    order_line._onchange_quantity()
                    values = {}
                    for field_name in order_line._fields.keys():
                        values[field_name] = order_line[field_name]
                    order_line.create(
                        order_line._convert_to_write(values))
        else:
            return super()._inverse_set_process_qty()
