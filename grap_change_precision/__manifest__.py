# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Change Precision",
    "version": "12.0.1.1.2",
    "summary": "Change the precisions names and values of some fields",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "sale_margin",
        # OCA
        "account_invoice_margin",
        "pos_margin",
        "product_standard_price_tax_included",
        # GRAP
        "account_invoice_supplierinfo_update_standard_price",
        "grap_change_base_product_mass_addition",
    ],
    "data": [
        "data/decimal_precision.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
    ],
    "installable": True,
}
