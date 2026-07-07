# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Point Of Sale",
    "version": "16.0.4.1.0",
    "category": "Web",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": ["point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/view_product_template.xml",
        "views/view_pos_session.xml",
        "views/view_pos_order_line.xml",
        "views/view_pos_order.xml",
        "views/menu.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "fermente_pos/static/src/scss/fermente_pos.scss",
        ],
    },
}
