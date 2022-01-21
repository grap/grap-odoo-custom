# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Change translation",
    "summary": "Disable the translation mechanism for a many" " fields",
    "version": "12.0.1.2.1",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "account",
        "base",
        "calendar",
        "delivery",
        "mail",
        "point_of_sale",
        "product",
        "sale_management",
        "stock",
        "uom",
        "utm",
        # OCA
        "account_product_fiscal_classification",
    ],
    "installable": True,
}
