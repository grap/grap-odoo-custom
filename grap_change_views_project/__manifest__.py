# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Mouna SEBTI (https://github.com/mounasb)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Project Views",
    "version": "12.0.1.0.5",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "project",
        # OCA
        "project_task_add_very_high",
        # GRAP
        "grap_cooperative",
    ],
    "data": [
        "views/templates.xml",
        "views/view_project_project.xml",
        "views/view_project_task.xml",
    ],
    "installable": True,
}
