# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Partner Views",
    "version": "12.0.0.0.12",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        # Odoo Modules
        "account",
        "contacts",
        "product",
        "stock",
        "purchase",
        "mail",
        "delivery",
        # OCA Modules
        "purchase_triple_discount",
    ],
    "data": [
        "views/view_res_partner_form.xml",
        "views/view_res_partner_tree.xml",
    ],
    "installable": True,
}
