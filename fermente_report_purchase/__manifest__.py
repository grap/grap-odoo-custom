# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Report adjustements for Purchase",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        # OCA
        "report_xlsx_helper",
        "purchase_triple_discount",
        # GRAP
        "fermente_report_base",
    ],
    "data": [
        "data/ir_actions_report.xml",
        "report/qweb_template_purchase_order.xml",
    ],
    "installable": True,
}
