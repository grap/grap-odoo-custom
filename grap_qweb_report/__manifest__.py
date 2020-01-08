# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Custom Qweb Reports",
    "version": "12.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        # "account",
        # "base_fiscal_company",
        # "base_company_legal_info",
        # "l10n_fr_siret",
        # "purchase",
        # "sale",
        # "sale_recovery_moment",
        # "product",
        "product_print_category",
        # "point_of_sale",
    ],
    "data": [
        "report/qweb_pricetag_square_small.xml",
        "report/qweb_pricetag_square_large.xml",
        "report/qweb_pricetag_normal_small.xml",
        "report/qweb_pricetag_normal_large.xml",
        "data/product_print_category.xml",
    ],
    "qweb": [],
    "installable": True,
}
