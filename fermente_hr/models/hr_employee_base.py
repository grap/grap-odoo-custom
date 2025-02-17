# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    @api.depends("resource_calendar_id", "hr_presence_state")
    def _compute_presence_icon(self):
        self.update(
            {
                "show_hr_icon_display": False,
                "hr_icon_display": "presence_to_define",
            }
        )
