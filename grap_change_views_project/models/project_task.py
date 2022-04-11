# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    github_link_1 = fields.Char(
        string="Pull request n°1", track_visibility="onchange"
    )  # max default size = 250
    github_link_2 = fields.Char(string="Pull request n°2", track_visibility="onchange")
    github_link_3 = fields.Char(string="Pull request n°3", track_visibility="onchange")
