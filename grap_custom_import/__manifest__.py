# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Custom Import",
    "summary": "Allow to make advanced custom imports of products, partners, etc...",
    "version": "12.0.1.0.1",
    "category": "GRAP Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        # Odoo
        "base_import",
        "point_of_sale",
        # OCA
        "purchase_triple_discount",
        # grap
        "recurring_consignment",
        "product_label",
        "product_print_category",
        "product_origin",
        "product_origin_l10n_fr_department",
    ],
    "installable": True,
}
