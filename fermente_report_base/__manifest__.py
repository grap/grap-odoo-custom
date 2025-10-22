# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Custom Qweb Reports",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "web",
        # OCA
        "base_company_legal_info",
        "l10n_fr_siret",
        # GRAP
        "fiscal_company_base",
        "product_food_certification",
    ],
    "data": [
        "report/qweb_template_layout_standard.xml",
        "data/report_paperformat.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "fermente_report_base/static/src/scss/**",
        ],
    },
    "installable": True,
}
