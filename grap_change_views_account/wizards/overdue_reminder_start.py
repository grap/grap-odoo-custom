# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class OverdueReminderStart(models.TransientModel):
    _inherit = "overdue.reminder.start"

    up_to_date = fields.Boolean(default=True)
