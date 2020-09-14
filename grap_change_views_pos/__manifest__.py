# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change POS Views",
    "version": "12.0.1.0.1",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
        "pos_multicompany",
        "pos_margin",
    ],
    "data": [
        "views/view_account_bank_statement.xml",
        "views/view_account_bank_statement_line.xml",
        "views/view_pos_category.xml",
        "views/view_pos_order.xml",
        "views/view_pos_order_line.xml",
        "views/view_pos_session.xml",
        "views/menu.xml",
        'views/templates.xml',
    ],
    "installable": True,
}
