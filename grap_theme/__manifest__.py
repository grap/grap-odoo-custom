# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Web Theme",
    "summary": "Customize Odoo web User Interface",
    "version": "12.0.1.2.0",
    "category": "GRAP Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "web",
        "web_favorite_company",
    ],
    "data": [
        "views/templates.xml",
    ],
    "qweb": [
        "static/src/xml/base.xml",
    ],
    "installable": True,
}
