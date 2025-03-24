# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange("purchase_ok")
    def _onchange_purchase_ok(self):
        buy_route_id = self.env.ref("purchase_stock.route_warehouse0_buy").id
        if self.purchase_ok:
            self.route_ids = [(4, buy_route_id)]
        else:
            self.route_ids = [(3, buy_route_id)]
