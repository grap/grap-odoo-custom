# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Partner Views",
    "version": "12.0.0.0.17",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "account",
        "contacts",
        "delivery",
        "mail",
        "product",
        "purchase",
        "sales_team",
        "stock",
        # OCA
        "purchase_triple_discount",
    ],
    "data": [
        "views/menu.xml",
        "views/view_res_partner_form.xml",
        "views/view_res_partner_tree.xml",
    ],
    "installable": True,
}
