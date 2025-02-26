# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FoodMenu(models.Model):
    _inherit = "mrp.food.menu"

    food_menu_tag_ids = fields.Many2many(
        string="Tags",
        comodel_name="mrp.food.menu.tag",
        help="Choose or create your tags for your Food Menu and set its color.",
    )
