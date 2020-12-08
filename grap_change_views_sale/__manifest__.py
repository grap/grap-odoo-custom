# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT <quentin.dupont@grap.coop>
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Sale Views",
    "version": "12.0.1.0.6",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "delivery",
        "sale_margin",
        "product_margin_classification",
    ],
    "data": [
        "views/menu.xml",
        "views/view_sale_order.xml",
    ],
    "installable": True,
}
