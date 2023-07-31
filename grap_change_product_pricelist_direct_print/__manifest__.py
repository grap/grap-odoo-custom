# Copyright (C) 2023-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Product Pricelist Direct Print",
    "version": "12.0.1.0.0",
    "category": "GRAP - Custom",
    "summary": "Display custom fields in Pricelist report",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        # OCA
        "product_pricelist_direct_print",
        # GRAP
        "sale_eshop",
    ],
    "data": [
        "reports/report_product_pricelist.xml",
        "wizards/view_product_pricelist_print.xml",
    ],
    "installable": True,
}
