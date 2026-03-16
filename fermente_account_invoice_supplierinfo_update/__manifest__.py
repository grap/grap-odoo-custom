# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Quentin DUPONT <quentin.dupont@grap.coop>
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fermente - Change Views Account Invoice Supplierinfo Update",
    "version": "16.0.1.2.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        # OCA
        "account_invoice_supplierinfo_update_qty_multiplier",
        "web_tree_dynamic_colored_field",
        # GRAP
        "account_invoice_supplierinfo_update_standard_price",
    ],
    "data": [
        "wizards/view_wizard_update_invoice_supplierinfo.xml",
        "views/account_invoice_view.xml",
    ],
    "installable": True,
}
