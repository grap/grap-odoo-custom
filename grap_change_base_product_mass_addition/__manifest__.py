# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Base Product Mass Addition",
    "version": "12.0.0.1.2",
    "category": "GRAP - Custom",
    "summary": "Fix slow call to odoo.tests.Form, used in "
    "base_product_mass_addition, for purchase_quick module",
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
