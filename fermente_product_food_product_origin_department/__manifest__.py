# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Product Food x Product origin",
    "version": "16.0.1.0.0",
    "category": "Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "product_food",
        "product_origin",
        "l10n_fr_department_product_origin",
    ],
    "data": [
        "views/view_product_product.xml",
        "views/view_product_template.xml",
    ],
}
