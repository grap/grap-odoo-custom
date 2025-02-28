# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fermente - Custom Web",
    "summary": "Customize Odoo web User Interface",
    "version": "16.0.1.0.0",
    "category": "Fermente Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": ["web"],
    "assets": {
        "web.assets_backend": [
            "fermente_web/static/src/xml/switch_company_menu.xml",
            "fermente_web/static/src/js/switch_company_menu.esm.js",
            "fermente_web/static/src/scss/fermente_web.scss",
        ],
    },
    # "qweb": [
    #     "static/src/xml/base.xml",
    # ],
    "installable": True,
}
