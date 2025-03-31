# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Food Openfoodfacts",
    "summary": "Link Openfoodfact database with Odoo models",
    "version": "12.0.1.1.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # GRAP
        "mrp_food",
        "mrp_business",
    ],
    "data": [
        # "views/menu.xml",
        "views/product_product.xml",
    ],
    "external_dependencies": {
        "python": ["openfoodfacts"],
    },
    "installable": True,
}
