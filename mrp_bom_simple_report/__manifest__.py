# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP BoM Simple Report",
    "summary": "Print simple report for your Bill of Materials",
    "version": "12.0.1.0.1",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
    ],
    "data": [
        "data/report_paperformat.xml",
        "report/report_simple_bom.xml",
        "report/ir_actions_report.xml",
        "views/assets.xml",
    ],
    "installable": True,
}
