# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Views",
    "version": "12.0.1.1.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "grap_cooperative",
        "grap_change_views_product",
        "contacts",
        "purchase",
        "stock",
        "sale",
        "point_of_sale",
        "account",
        "mobile_kiosk_abstract",
        # For hidden items
        "utm",
        "mail",
        "calendar",
        "knowledge",
        "web_dashboard_tile",
        # Obsolete dependencies to remove after the migration
        "grap_change_views_account",
        "grap_change_views_base",
        "grap_change_views_pos",
        "grap_change_views_purchase",
        "grap_change_views_sale",
    ],
    "data": [
        "views/menu.xml",
    ],
    "installable": True,
}
