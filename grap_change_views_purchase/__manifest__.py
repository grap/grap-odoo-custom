# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT <quentin.dupont@grap.coop>
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Purchase Views",
    "version": "12.0.3.0.3",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        # OCA
        "purchase_batch_invoicing",
        "purchase_discount",
        "purchase_triple_discount",
        # GRAP
        "intercompany_trade_purchase",
        "recurring_consignment_purchase",
    ],
    "data": [
        "views/menu.xml",
        "views/view_purchase_order.xml",
    ],
    "post_init_hook": "configure_product_template_purchase_method",
    "installable": True,
}
