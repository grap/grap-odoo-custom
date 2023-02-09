# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # Column Section
    # Percentage float, so 25% is 0,25. For one number behind decimal, needs 3 digits
    line_weight = fields.Float(
        string="Weight",
        compute="_compute_line_weight",
    )

    line_weight_percentage = fields.Float(
        string="Weight %",
        compute="_compute_line_weight_percentage",
        digits=(16, 3),
    )

    @api.depends("product_qty", "product_uom_id", "product_id")
    def _compute_line_weight(self):
        for line in self:
            if line.product_uom_id.category_id.measure_type == "weight":
                line.line_weight = line.product_qty / line.product_uom_id.factor
            else:
                line.line_weight = line.product_id.net_weight * line.product_qty

    @api.depends("product_qty", "bom_id.bom_line_ids.product_qty")
    def _compute_line_weight_percentage(self):
        for line in self:
            bom_total_weight = line.bom_id.bom_components_total_weight
            line.line_weight_percentage = (
                line.line_weight / bom_total_weight if bom_total_weight != 0 else 0
            )
