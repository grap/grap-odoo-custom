# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.onchange("type")
    def _onchange_type_purchase_method(self):
        if self.type == "service":
            self.purchase_method = "purchase"
        else:
            self.purchase_method = "receive"
