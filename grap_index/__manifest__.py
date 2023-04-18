# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Custom Index",
    "summary": "Add Extra postgresql Indexes",
    "version": "12.0.1.0.2",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        # Odoo
        "point_of_sale",
        "purchase_stock",
        "sale_stock",
    ],
    "installable": True,
    "uninstall_hook": "drop_indexes",
}
