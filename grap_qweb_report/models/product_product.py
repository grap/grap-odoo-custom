# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_supplierinfo_from_purchase_order_line(self, order_line):
        self.ensure_one()
        supplierinfos = order_line.product_id.seller_ids.filtered(
            lambda x: x.name == order_line.order_id.partner_id
            and (not x.product_id or x.product_id == order_line.product_id)
        )
        if len(supplierinfos) <= 1:
            return supplierinfos

        # Try to guess supplierinfo, from the code set in the order line name
        regex_result = re.search(r"\[(.+)\].*", order_line.name)
        if regex_result and len(regex_result.groups()) == 1:
            product_code = regex_result.groups()[0]
            supplierinfos = supplierinfos.filtered(
                lambda x: x.product_code == product_code
            )
            if len(supplierinfos) <= 1:
                return supplierinfos

        # The code has not been found or there is many supplierinfo with the same code
        # Fallback and return the first supplierinfo
        return supplierinfos.sorted(key=lambda x: x.min_qty)[0]
