# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FoodMenuLine(models.Model):
    _inherit = "mrp.food.menu.line"

    planned_date = fields.Date(
        string="Planned Date",
    )
