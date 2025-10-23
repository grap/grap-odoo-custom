# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product default route MRP",
    "version": "16.0.1.1.1",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
    ],
    "post_init_hook": "_hook_add_mrp_route_to_products_with_boms",
    "installable": True,
}
