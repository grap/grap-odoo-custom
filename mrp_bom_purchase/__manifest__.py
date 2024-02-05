# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP BoM Purchase",
    "summary": "Handle purchase from your Bill of Materials",
    "version": "12.0.1.3.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # GRAP
        "mrp_business",
        "mrp_bom_sale_product_margin",
    ],
    "data": [
        "data/report_paperformat.xml",
        "report/report_bom_purchase_list.xml",
        "report/ir_actions_report.xml",
        "wizard/view_bom_print_purchase_list_wizard.xml",
        "views/action.xml",
        "views/assets.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
