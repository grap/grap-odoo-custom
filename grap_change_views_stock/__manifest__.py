# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Stock Views",
    "version": "12.0.0.1.3",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "stock_account",
        # GRAP
        "stock_inventory_merge",
    ],
    "data": [
        "views/view_stock_inventory.xml",
        "views/view_stock_inventory_line.xml",
        "views/view_stock_move.xml",
        "views/view_stock_picking.xml",
        "views/menu.xml",
        "views/action.xml",
    ],
    "installable": True,
}
