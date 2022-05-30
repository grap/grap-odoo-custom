# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductAllergen(models.Model):
    _inherit = "product.allergen"

    bom_ids = fields.Many2many(
        comodel_name="mrp.bom",
        inverse_name="bom_allergen_ids",
    )

    bom_qty = fields.Integer(
        string="BoM Quantity", compute="_compute_bom_qty", store=True
    )

    @api.depends("bom_ids")
    def _compute_bom_qty(self):
        for allergen in self:
            allergen.bom_qty = len(allergen.bom_ids)
