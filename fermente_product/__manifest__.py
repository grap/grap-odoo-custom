# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Product",
    "version": "16.0.2.0.0",
    "category": "Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "views/view_product_product.xml",
        "views/view_product_product.xml",
    ],
    "pre_init_hook": "configure_decimal_precision",
}
