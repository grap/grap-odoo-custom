# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Accesses",
    "version": "12.0.1.0.0",
    "summary": "Create role for users, add new groups for specific"
    " models and change accesses for a number of models.",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        # Odoo Modules
        "base_user_role",
        "point_of_sale",
        "purchase",
        "sales_team",
        "stock",
        # OCA Modules
        "bi_sql_editor",
        "pos_place",
        # GRAP Modules
        "intercompany_trade_base",
        "product_print_category",
        "product_to_scale_bizerba",
        "sale_recovery_moment",
        "stock_preparation_category",
    ],
    "data": [
        "security/ir_module_category.xml",
        "security/res_groups.xml",
        "data/res_users_role.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
        "demo/res_users.xml",
    ],
    "installable": True,
}
