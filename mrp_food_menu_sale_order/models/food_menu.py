# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FoodMenu(models.Model):
    _inherit = "mrp.food.menu"

    sale_order_ids = fields.One2many(
        comodel_name="sale.order",
        help="Theses sales were created from this menu.",
        inverse_name="food_menu",
        readonly=True,
    )

    sale_order_count = fields.Integer(
        string="Sale orders",
        compute="_compute_sale_order_count",
    )

    # Action Section
    def create_sale_order_from_menu(self):
        self.ensure_one()
        sale_order_line = []

        # Prepare sale.order.line with same order
        for line in sorted(self.menu_line_ids, key=lambda x: x.sequence):
            futur_order_line_vals = {
                "sequence": line.sequence,
                "display_type": line.display_type,
                "product_id": line.product_id.id,
                "name": line.product_id.name if line.product_id else line.name,
                "product_uom_qty": line.product_uom_qty,
                "product_uom": line.product_uom_id.id,
                "price_unit": line.product_id.list_price,
            }
            sale_order_line.append((0, 0, futur_order_line_vals))

        # Return sale.order Form view with values
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "view_mode": "form",
            "view_type": "form",
            "target": "current",
            "context": {
                "default_partner_id": False,
                "default_order_line": sale_order_line,
                "default_food_menu": self.id,
            },
        }

    @api.depends("sale_order_ids")
    def _compute_sale_order_count(self):
        for food_menu in self:
            food_menu.sale_order_count = len(food_menu.sale_order_ids)

    def action_view_sale_order(self):
        return self._get_action_view_picking(self.picking_ids)
