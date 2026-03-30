# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Project",
    "version": "16.0.2.1.0",
    "category": "Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": ["project"],
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/view_project_task.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "fermente_project/static/src/scss/fermente_project.scss",
        ],
    },
}
