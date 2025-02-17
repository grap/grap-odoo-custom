# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Business Modules",
    "summary": "MRP functions that meet the business needs of GRAP,"
    "adapted for food-related professions",
    "version": "16.0.1.1.1",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "mrp_product_produce_delay_in_hour",
    ],
    "demo": [
        "demo/product.xml",
        "demo/bom.xml",
    ],
    "installable": True,
}
