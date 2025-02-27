# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Food Menu Simple Report",
    "summary": "todo",
    "version": "16.0.1.0.0",
    "category": "Manufacturing",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["quentinDupont"],
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "mrp_food_menu_allergen",
    ],
    "assets": {
        "web.report_assets_common": [
            "/mrp_food_menu_simple_report/static/src/scss/mrp_food_menu_simple_report.scss"
        ],
    },
    "data": [
        "data/report_paperformat.xml",
        "report/report_simple_bom.xml",
        "report/ir_actions_report.xml",
    ],
    "installable": True,
}
