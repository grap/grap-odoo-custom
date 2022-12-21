# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Supplierinfo Update Standard Price Main Seller",
    "version": "12.0.1.0.1",
    "category": "GRAP Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        # GRAP
        "account_invoice_supplierinfo_update_standard_price",
        "product_main_seller",
    ],
    "data": [
        "wizard/wizard_update_invoice_supplierinfo.xml",
    ],
    "auto_install": True,
    "installable": True,
}
