# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Change Default",
    "version": "12.0.1.1.4",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "product",
        "point_of_sale",
        # OCA
        "pos_tare",
        "pos_order_to_sale_order",
        "pos_meal_voucher",
        # GRAP
        "joint_buying_product",
    ],
    "installable": True,
}
