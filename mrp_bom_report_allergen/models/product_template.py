# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Column Section
    meal_category_id = fields.Many2one(
        comodel_name="mrp.meal.category",
        string="Meal category",
        help="Add a Meal Category to order Products in BoM Allergens Table"
        ". E.g. starter, main course, dessert",
    )
