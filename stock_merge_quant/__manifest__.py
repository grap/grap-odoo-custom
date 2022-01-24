# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock - Merge Quants Tools",
    "version": "12.0.1.1.2",
    "category": "Tools",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        # GRAP
        # Depends on this module only to add a button in the correct place
        "grap_change_views_product",
    ],
    "data": [
        "data/ir_cron.xml",
        "views/view_product_product.xml",
    ],
    "external_dependencies": {
        "python": ["openupgradelib"],
    },
    "installable": True,
}
