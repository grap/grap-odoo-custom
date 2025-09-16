# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Custom Message on Reports",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "account",
        "purchase",
        "sale",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/view_report_custom_message.xml",
        "report/qweb_template_account_invoice.xml",
        "report/qweb_template_purchase_order.xml",
        "report/qweb_template_sale_order.xml",
        "report/qweb_template_stock_picking.xml",
    ],
    "demo": [
        "demo/report_custom_message.xml",
    ],
    "installable": True,
}
