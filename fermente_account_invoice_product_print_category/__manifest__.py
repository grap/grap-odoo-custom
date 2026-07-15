# Copyright (C) 2026-Today: GRAP (https://www.grap.coop)
# @author Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fermente - Account Invoice x Product Print Category",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "account",
        "product_print_category",
        # just for supplierinfo_ok
        "account_invoice_supplierinfo_update",
    ],
    "data": [
        "wizards/view_product_print_wizard.xml",
        "views/account_move_view.xml",
    ],
    "installable": True,
}
