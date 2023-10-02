# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Mouna SEBTI (https://github.com/mounasb)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


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

    requesting_company_ids = fields.Many2many(
        comodel_name="res.company", string="Requesting Companies"
    )

    requesting_people_ids = fields.Many2many(
        comodel_name="grap.people", string="Requesting Persons"
    )

    @api.onchange("requesting_people_ids")
    def _onchange_requesting_people_ids(self):
        to_add = self.requesting_people_ids.mapped("company_id").filtered(
            lambda x: x.id not in self.requesting_company_ids.ids
        )
        self.requesting_company_ids += to_add
