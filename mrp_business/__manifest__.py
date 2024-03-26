# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Business Modules",
    "summary": "MRP functions that meet the business needs of GRAP,"
    "adapted for food-related professions",
    "version": "12.0.1.5.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # OCA modules
        "product_net_weight",
        "res_company_code",
        "web_notify",
        # GRAP Modules
        "mrp_bom_line_net_qty",
        "mrp_bom_product_variant",
    ],
    "demo": [
        "demo/product.xml",
        "demo/bom.xml",
    ],
    "data": [
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "views/view_mrp_bom.xml",
        "views/view_mrp_meal_category.xml",
        "views/view_product_product.xml",
    ],
    "installable": True,
}
