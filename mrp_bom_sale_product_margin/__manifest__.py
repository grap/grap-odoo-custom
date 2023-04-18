# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP BoM Sale Product Margin",
    "summary": "Handle Sale price for product's bom with margin",
    "version": "12.0.1.1.5",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # OCA modules
        "product_standard_margin",
        "product_margin_classification",
        "web_notify",
        # GRAP modules,
    ],
    "data": [
        "views/view_mrp_bom.xml",
    ],
    "installable": True,
}
