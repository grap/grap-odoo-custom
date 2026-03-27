# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_displayed_in_directory = fields.Boolean(
        string="Displayed in Directory", default=True, groups="hr.group_hr_user"
    )
