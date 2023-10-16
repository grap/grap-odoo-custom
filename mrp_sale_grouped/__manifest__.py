# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Grouped Sales and Production",
    "summary": "Quickly manage what you need to produce thanks to grouped sales",
    "version": "12.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "sale_management",
        # OCA
        "web_widget_x2many_2d_matrix",
        "sale_mrp_link",
        # GRAP
        "mrp_bom_simple_report",
        "mrp_bom_purchase",
    ],
    "data": [
        "data/report_paperformat.xml",
        "security/ir.model.access.csv",
        "report/ir_actions_report.xml",
        "report/report_sale_grouped.xml",
        "views/action.xml",
        "views/view_mrp_sale_grouped.xml",
        "views/view_sale_order.xml",
        "wizard/view_sale_grouped_wizard.xml",
        "wizard/x2m_matrix_grouped_sales.xml",
        "views/action.xml",
    ],
    "installable": True,
}
