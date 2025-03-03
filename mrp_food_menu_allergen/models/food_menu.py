# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FoodMenu(models.Model):
    _inherit = "mrp.food.menu"

    menu_allergen_ids = fields.Many2many(
        string="Allergens",
        comodel_name="product.allergen",
        help="Includes BoMs allergens",
        compute="_compute_menu_allergen_ids",
        store=True,
    )

    @api.depends("menu_line_ids", "menu_line_ids.bom_id.bom_allergen_ids")
    def _compute_menu_allergen_ids(self):
        for food_menu in self:
            # list(set()) removes duplication
            food_menu.menu_allergen_ids = [
                (
                    6,
                    0,
                    list(
                        set(
                            [
                                x.id
                                for food_menu_line in food_menu.menu_line_ids
                                for x in food_menu_line.bom_id.bom_allergen_ids
                            ]
                        )
                    ),
                )
            ]
