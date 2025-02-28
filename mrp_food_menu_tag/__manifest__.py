# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Food Menu Tag",
    "summary": "Add tags on your Food Menu to classify them.",
    "version": "16.0.1.0.0",
    "category": "Manufacture",
    "author": "GRAP, , Odoo Community Association (OCA)",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
    ],
    "demo": ["demo/mrp_food_menu_tag.xml"],
    "data": [
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "views/view_mrp_food_menu.xml",
        "views/view_mrp_food_menu_tag.xml",
    ],
    "installable": True,
}
