# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FoodMenu(models.Model):
    _inherit = "mrp.food.menu"

    purchase_order_ids = fields.One2many(
        comodel_name="purchase.order",
        help="Theses purchase orders were created from this menu.",
        inverse_name="food_menu",
        readonly=True,
    )

    purchase_order_count = fields.Integer(
        string="Purchase orders",
        compute="_compute_purchase_order_count",
    )

    @api.depends("purchase_order_ids")
    def _compute_purchase_order_count(self):
        for food_menu in self:
            food_menu.purchase_order_count = len(food_menu.purchase_order_ids)

    def action_view_purchase_order(self):
        return self._get_action_view_picking(self.picking_ids)
