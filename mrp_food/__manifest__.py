# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP for Food",
    "summary": "MRP modules adapted for food-related professions",
    "version": "12.0.1.1.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # "purchase",
        # "sale_mrp",
        # OCA modules
        "product_food",
        "product_label",
        "web_widget_color",
        # GRAP modules,
        "product_main_seller",
    ],
    "demo": [
        "demo/allergens.xml",
        "demo/seasonality.xml",
        "demo/seasonality_line.xml",
        "demo/product.xml",
        "demo/bom.xml",
        "demo/res_groups.xml",
    ],
    "data": [
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "views/view_mrp_bom.xml",
        "views/view_product_allergen.xml",
        "views/view_product_product.xml",
        "views/view_product_template.xml",
        "views/view_seasonality.xml",
    ],
    "images": [
        "./static/img/tomato_pie.png",
    ],
    "installable": True,
}
