# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # Column Section
    description_packaging = fields.Char(string="Packaging description")
    # Tracking not easily possible for One2many in v16
    # bom_line_ids = fields.One2many(tracking=True)
    # TODO v16 module dédié
    # priority = fields.Selection(
    #     [("0", "Low"), ("1", "Normal"), ("2", "High"), ("3", "Very High")],
    #     string="Priority",
    #     default="0",
    #     help="Helps prioritize BoM.",
    # )
    meal_category_id = fields.Many2one(
        related="product_id.meal_category_id",
        string="Meal category",
    )

    # ========== Fields for mrp_bom_weight → TODO v16 voir où le mettre
    # diff_bom_qty_and_net_quantities = fields.Float(
    #     digits="Product Price",
    #     compute="_compute_diff_bom_qty_and_net_quantities",
    # )
