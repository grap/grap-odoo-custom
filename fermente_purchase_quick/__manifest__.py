# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fermente - Purchase Quick",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "summary": "Add extra fields in quick purchase tree view",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        # OCA
        "purchase_quick",
        "product_supplierinfo_qty_multiplier",
        "purchase_triple_discount",
        "web_tree_dynamic_colored_field",
    ],
    "data": ["views/view_product_product.xml"],
    "installable": True,
}
