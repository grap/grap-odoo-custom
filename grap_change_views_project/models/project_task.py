# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Mouna SEBTI (https://github.com/mounasb)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    github_link_1 = fields.Char(string="Pull request n°1")
    github_link_2 = fields.Char(string="Pull request n°2")
    github_link_3 = fields.Char(string="Pull request n°3")

    is_odoo_development = fields.Boolean(
        "Odoo Development", related="project_id.is_odoo_development"
    )

    modules_to_install = fields.Char("Modules to install")
    modules_to_uninstall = fields.Char("Modules to uninstall")
    sql_request = fields.Text("SQL request")

    user_id = fields.Many2one(default=None)
