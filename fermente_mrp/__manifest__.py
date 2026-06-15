# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - MRP",
    "version": "16.0.1.3.1",
    "category": "Web",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": ["mrp"],
    "data": [
        "views/menu.xml",
        "views/mrp_production_view.xml",
        "security/ir.model.access.csv",
        "data/stock_route.xml",
    ],
}
