# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fermente - Change Base Product Mass Addition",
    "version": "16.0.1.0.0",
    "category": "Custom",
    "summary": "Add purchase fields to Product Mass Addition",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        # OCA
        "base_product_mass_addition",
        "purchase_quick",
        "onchange_helper",
        "product_supplierinfo_qty_multiplier",
        "purchase_discount",
        "purchase_triple_discount",
    ],
    "data": [
        "views/view_product_product.xml",
    ],
    "installable": True,
}
