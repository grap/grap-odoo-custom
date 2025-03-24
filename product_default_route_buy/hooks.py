# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID, api


def _hook_add_buy_route_to_purchase_ok_products(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    buy_route = env.ref("purchase_stock.route_warehouse0_buy", raise_if_not_found=True)

    if buy_route:
        products = env["product.template"].search([("purchase_ok", "=", True)])
        for product in products:
            product.route_ids = [(4, buy_route.id)]
