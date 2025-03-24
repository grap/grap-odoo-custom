# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Point Of Sale Restaurant",
    "version": "16.0.2.0.0",
    "category": "Web",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": ["pos_restaurant", "fermente_pos"],
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/view_pos_config.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "fermente_pos_restaurant/static/src/xml/FloorScreen.xml",
        ],
    },
}
