# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - MRP Manufacture for Food",
    "summary": "MRP modules adapted for food-related professions",
    "version": "12.0.1.1.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "purchase",
        "product",
        "sale_mrp",
        # OCA modules
        "web_widget_color",
        "product_food",
        "product_label",
    ],
    "data": [
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "views/view_mrp_bom.xml",
        "views/view_mrp_bom_tag.xml",
        "views/view_mrp_bom_season.xml",
        "views/view_product_product.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
