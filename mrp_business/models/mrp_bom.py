# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

from odoo.addons import decimal_precision as dp


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # ========== Divers
    currency_id = fields.Many2one(related="product_tmpl_id.currency_id")
    description_packaging = fields.Char(string="Packaging description")
    # Tracking not possible for One2many
    # bom_line_ids = fields.One2many(track_visibility="onchange")
    priority = fields.Selection(
        [("0", "Low"), ("1", "Normal"), ("2", "High"), ("3", "Very High")],
        string="Priority",
        default="0",
        help="Helps prioritize BoM.",
    )
    meal_category_id = fields.Many2one(
        related="product_id.meal_category_id",
        string="Meal category",
    )

    # ========== Fields for Time
    time_to_produce = fields.Float(help="Time in hour to produce this BoM.", store=True)
    # ========== Fields for mrp_bom_line_net_qty
    diff_bom_qty_and_net_quantities = fields.Float(
        digits=dp.get_precision("Product Price"),
        compute="_compute_diff_bom_qty_and_net_quantities",
    )
