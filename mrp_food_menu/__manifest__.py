# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Food Menu",
    "summary": "Base model to create Menu and its components.",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "account",
    ],
    "demo": [
        "demo/product_product.xml",
        "demo/mrp_food_menu.xml",
    ],
    "data": [
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "views/view_food_menu.xml",
    ],
    "installable": True,
}
