# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from random import randint

from odoo import _, api, fields, models


class FoodMenuTag(models.Model):
    _name = "mrp.food.menu.tag"
    _description = "MRP Food Menu Tag"
    _parent_name = "parent_id"
    _parent_store = True
    _order = "complete_name"

    def _default_color(self):
        return randint(1, 11)

    # Column Section
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda s: s._default_company_id(),
    )

    name = fields.Char(required=True)
    color = fields.Integer(default=lambda self: self._default_color())
    complete_name = fields.Char(
        compute="_compute_complete_name", store=True, recursive=True
    )

    parent_id = fields.Many2one(
        "mrp.food.menu.tag", "Parent Menu Tag", index=True, ondelete="cascade"
    )
    parent_path = fields.Char(index=True, unaccent=False)
    child_id = fields.One2many("mrp.food.menu.tag", "parent_id", "Child Categories")

    food_menu_ids = fields.Many2many(
        comodel_name="mrp.food.menu",
    )

    food_menu_qty = fields.Integer(
        "Food Menu Quantity",
        compute="_compute_food_menu_qty",
        help="Number of menus with this menu tag (not considering children categories)",
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for food_menu_tag in self:
            if food_menu_tag.parent_id:
                food_menu_tag.complete_name = _("%(complete_name)s / %(name)s") % (
                    {
                        "complete_name": food_menu_tag.parent_id.complete_name,
                        "name": food_menu_tag.name,
                    }
                )
            else:
                food_menu_tag.complete_name = food_menu_tag.name

    @api.depends("food_menu_ids")
    def _compute_food_menu_qty(self):
        for food_menu_tag in self:
            food_menu_tag.food_menu_qty = len(food_menu_tag.food_menu_ids)

    # Model Section
    @api.model
    def _default_company_id(self):
        return self.env.company.id

    # Name Section
    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get("display_complete_name", False):
                result.append((record.id, record.complete_name))
            else:
                result.append((record.id, record.name))
        return result
