# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Mouna SEBTI (https://github.com/mounasb)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    description = fields.Html(string="Description")

    is_odoo_development = fields.Boolean(string="Odoo Development")
