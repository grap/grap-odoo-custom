# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT <quentin.dupont@grap.coop>
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Purchase Views",
    "version": "12.0.1.1.3",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "purchase_batch_invoicing",
        "purchase",
        "purchase_discount",
        "purchase_triple_discount",
        "intercompany_trade_purchase",
        "recurring_consignment",
    ],
    "data": [
        "views/menu.xml",
        "views/view_purchase_order.xml",
    ],
    "installable": True,
}
