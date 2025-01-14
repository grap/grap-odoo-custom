# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP BoM Print",
    "summary": "Manage the various useful prints for Bill of Materials",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # GRAP
        "mrp_bom_product_allergen",
    ],
    "data": [
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "data/report_paperformat.xml",
        "report/report_bom_allergens.xml",
        "report/ir_actions_report.xml",
        "views/view_mrp_bom.xml",
        "views/view_mrp_meal_category.xml",
        "views/view_product_template.xml",
        "wizard/view_bom_print_wizard.xml",
        "views/menu.xml",
    ],
    "assets": {
        'web.report_assets_common': [
            'mrp_bom_report_allergen/static/src/scss/mrp_bom_report_allergen.scss',
        ],
    },
    "installable": True,
}
