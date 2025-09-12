# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Custom Qweb Reports",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "web",
        # GRAP
        "product_food_certification",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/view_report_custom_message.xml",
        "report/qweb_template_layout_standard.xml",
        "data/report_paperformat.xml",
    ],
    "demo": [
        "demo/report_custom_message.xml",
    ],
    "installable": True,
}
