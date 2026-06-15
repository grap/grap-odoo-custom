# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Sale",
    "version": "16.0.2.3.0",
    "category": "Web",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": ["sale", "sales_team", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/view_sale_order.xml",
        "views/view_product_template.xml",
    ],
}
