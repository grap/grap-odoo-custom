# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FoodMenu(models.Model):
    _name = "mrp.food.menu"
    _description = "Food menu"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        help="Menu name",
        required=True,
    )

    description = fields.Char(help="Field for external use, for example for PDF.")

    internal_notes = fields.Char(help="Field for internal use only.")

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda s: s._default_company_id(),
    )

    menu_line_ids = fields.One2many(
        comodel_name="mrp.food.menu.line",
        inverse_name="menu_id",
    )

    # Quick access to Products without any BoM
    product_wo_bom_ids = fields.One2many(
        comodel_name="product.product",
        compute="_compute_product_wo_bom_ids",
    )

    product_wo_bom_qty = fields.Integer(
        compute="_compute_product_wo_bom_qty",
    )

    # Methods for Products without any BoM
    @api.depends("menu_line_ids")
    def _compute_product_wo_bom_ids(self):
        for food_menu in self:
            food_menu.product_wo_bom_ids = food_menu.mapped(
                "menu_line_ids.product_id"
            ).filtered(lambda r: r.bom_count == 0)

    @api.depends("product_wo_bom_ids")
    def _compute_product_wo_bom_qty(self):
        for food_menu in self:
            food_menu.product_wo_bom_qty = len(food_menu.product_wo_bom_ids)

    # Default methods
    @api.model
    def _default_company_id(self):
        return self.env.company
