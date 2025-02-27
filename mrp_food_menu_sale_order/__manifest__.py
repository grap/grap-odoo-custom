# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Food Menu Sale Order",
    "summary": "Create a sale order directly from your food menu.",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp_food_menu",
        "sale",
    ],
    "data": [
        "views/view_food_menu.xml",
        "views/view_sale_order.xml",
    ],
    "installable": True,
}
