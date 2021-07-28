# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Partner Views",
    "version": "12.0.0.0.13",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "account",
        "base",
        "contacts",
        "delivery",
        "purchase",
        "product",
        "stock",
    ],
    "data": [
        "views/view_res_partner.xml",
        "views/view_res_partner_tree.xml",
    ],
    "installable": True,
}
