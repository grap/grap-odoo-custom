# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # Percentage float, so 25% is 0,25. For one number behind decimal, needs 3 digits
    line_gross_weight = fields.Float(
        string="Gross weight",
        compute="_compute_line_gross_weight",
        digits=dp.get_precision("Product Unit of Measure"),
    )
    line_net_weight = fields.Float(
        string="Net weight",
        compute="_compute_line_net_weight",
        digits=dp.get_precision("Product Unit of Measure"),
    )
    line_net_weight_percentage = fields.Float(
        string="Net weight %",
        compute="_compute_line_net_weight_percentage",
        digits=(16, 3),
    )

    # Line weight
    @api.depends(
        "product_qty_net", "product_uom_id", "product_id", "product_id.net_weight"
    )
    def _compute_line_net_weight(self):
        for line in self:
            if line.product_uom_id.category_id.measure_type == "weight":
                line.line_net_weight = line.product_qty_net / line.product_uom_id.factor
            else:
                line.line_net_weight = line.product_id.net_weight * line.product_qty_net

    @api.depends("product_qty_net", "product_uom_id", "product_id", "product_id.weight")
    def _compute_line_gross_weight(self):
        for line in self:
            if line.product_uom_id.category_id.measure_type == "weight":
                line.line_gross_weight = line.product_qty / line.product_uom_id.factor
            else:
                line.line_gross_weight = line.product_id.weight * line.product_qty_net

    @api.depends("product_qty_net", "bom_id.bom_line_ids.product_qty_net")
    def _compute_line_net_weight_percentage(self):
        for line in self:
            bom_total_weight = line.bom_id.bom_components_total_net_weight
            line.line_net_weight_percentage = (
                line.line_net_weight / bom_total_weight if bom_total_weight != 0 else 0
            )
