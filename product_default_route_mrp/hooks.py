# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def _hook_add_mrp_route_to_products_with_boms(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    mrp_route = env.ref("mrp.route_warehouse0_manufacture", raise_if_not_found=True)

    if mrp_route:
        _logger.info("[product_default_route_mrp] Initialize products with MRP route")
        products = env["product.template"].search([])
        for product in products:
            has_bom = (
                env["mrp.bom"].search_count([("product_tmpl_id", "=", product.id)]) > 0
            )
            if has_bom:
                product.route_ids = [(4, mrp_route.id)]
