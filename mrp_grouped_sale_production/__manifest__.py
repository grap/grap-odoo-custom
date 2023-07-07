# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Grouped Sales and Production",
    "summary": "Quickly see what you need to produce thanks to grouped sales",
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
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/view_mrp_grouped_sale_production.xml",
        "views/view_sale_order.xml",
        "wizard/x2m_matrix_grouped_sales.xml",
    ],
    "installable": True,
}
