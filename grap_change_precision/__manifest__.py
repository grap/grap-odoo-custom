# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Change Precision",
    "version": "12.0.1.0.4",
    "summary": "Change the precisions names and values of some fields",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "account_invoice_margin",
        "pos_margin",
        "sale_margin",
        "product_standard_price_tax_included",
        "grap_change_base_product_mass_addition",
        "account_invoice_supplierinfo_update_standard_price",
    ],
    "data": [
        "data/decimal_precision.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
    ],
    "installable": True,
}
