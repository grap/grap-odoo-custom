# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP BoM Print",
    "summary": "Manage the various useful prints for Bill of Materials",
    "version": "12.0.1.1.1",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # GRAP
        "mrp_food",
        "mrp_business",
    ],
    "data": [
        "data/report_paperformat.xml",
        "report/report_bom_allergens.xml",
        "report/ir_actions_report.xml",
        "wizard/view_bom_print_wizard.xml",
        "views/action.xml",
        "views/assets.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
