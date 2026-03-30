# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MRP BoM Simulate Quantities",
    "version": "16.0.1.1.2",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
    ],
    "demo": [
        "demo/product_product_demo.xml",
        "demo/mrp_bom_demo.xml",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_bom.xml",
    ],
    "installable": True,
}
