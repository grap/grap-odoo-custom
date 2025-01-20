# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP BoM Wizard production",
    "summary": "Wizard linked to Bill of Materials to help your production.",
    "version": "16.0.1.1.0",
    "category": "Manufacturing",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        # OCA modules
        "mrp_bom_simple_packaging_description",
        "mrp_bom_product_price_margin",
        "mrp_bom_simple_report",
        "mrp_bom_simple_packaging_description",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/report_paperformat.xml",
        "report/report_bom_wizard_production.xml",
        "report/ir_actions_report.xml",
        "wizard/view_bom_wizard_production.xml",
        "views/action.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "mrp_bom_wizard_production/static/src/scss/mrp_bom_wizard_production.scss",
        ],
    },
    "installable": True,
}
