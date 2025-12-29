# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Food Menu Purchase Order",
    "summary": "Create purchase orders directly from your food menu.",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp_food_menu",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/action.xml",
        "views/view_food_menu.xml",
        "views/view_purchase_order.xml",
        "wizard/view_food_menu_wizard_purchase_order.xml",
    ],
    "installable": True,
}
