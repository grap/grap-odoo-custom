# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Grouped Sales and Production",
    "summary": "Quickly manage what you need to produce thanks to grouped sales",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "sale_mrp",
        # OCA
        "web_widget_x2many_2d_matrix",
        "mrp_bom_simple_report",
        "mrp_bom_wizard_production",
        # GRAP
    ],
    "demo": [
        "demo/product.xml",
        "demo/bom.xml",
        "demo/sale_order.xml",
        "demo/sale_order_line.xml",
        "demo/mrp_sale_grouped.xml",
    ],
    "data": [
        "data/report_paperformat.xml",
        "data/stock_route.xml",
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "report/report_sale_grouped.xml",
        "report/ir_actions_report.xml",
        "views/action.xml",
        "views/menu.xml",
        "views/view_mrp_sale_grouped.xml",
        "views/view_sale_order.xml",
        "wizard/view_sale_grouped_wizard.xml",
        "wizard/x2m_matrix_grouped_sales.xml",
        "wizard/view_production_assistant_wizard.xml",
    ],
    "installable": True,
}
