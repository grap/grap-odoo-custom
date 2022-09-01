# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBomCategory(models.Model):
    _name = "mrp.bom.meal.category"
    _description = "MRP BoM Meal Category"

    # Column Section
    name = fields.Char(
        string="Meal Category",
        required=True,
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda s: s._default_company_id(),
    )

    sequence = fields.Integer(
        default=10, help="Order Meal Category. Used for printing documents"
    )

    _sql_constraints = [
        ("name_unique", "unique(name)", "Category name already exists"),
    ]

    # Default methods
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id
