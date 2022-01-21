# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Change Data",
    "version": "12.0.1.0.9",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "delivery",
        "product",
        "point_of_sale",
        # OCA
        "product_category_active",
        # GRAP
        "grap_change_translation",
    ],
    "data": [
        "data/barcode_nomenclature.xml",
        "data/product_category.xml",
        "data/product_product.xml",
        "data/res_country_group.xml",
        "data/uom_uom.xml",
    ],
    "installable": True,
}
