# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change POS Views",
    "version": "12.0.1.1.5",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
        "pos_cash_rounding",
        # OCA
        "pos_margin",
        "pos_cash_move_reason",
        # GRAP
        "pos_multicompany",
    ],
    "data": [
        "views/view_account_bank_statement.xml",
        "views/view_account_bank_statement_line.xml",
        "views/view_pos_category.xml",
        "views/view_pos_order.xml",
        "views/view_pos_order_line.xml",
        "views/view_pos_session.xml",
        "views/view_pos_config.xml",
        "views/menu.xml",
        "views/templates.xml",
    ],
    "installable": True,
}
