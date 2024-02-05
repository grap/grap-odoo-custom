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
    product_qty_net = fields.Float(
        string="Net quantity",
        help="Weight after any preparation, e.g. weight of carrots after they are grated ",
        digits=dp.get_precision("Product Unit of Measure"),
    )
    loss_percentage = fields.Float(
        string="Loss %",
        help="Percentage loss, for example, when grating carrots",
        digits=(16, 2),
    )
    diff_product_qty_gross_net = fields.Float(
        digits=dp.get_precision("Product Price"),
        compute="_compute_diff_product_qty_gross_net",
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

    # Functions to change product fields
    def calculate_qty_net_theoretical(self, product_qty_gross, loss_percentage):
        return (1 - loss_percentage / 100) * product_qty_gross

    @api.multi
    @api.depends("product_qty", "product_qty_net", "loss_percentage")
    def _compute_diff_product_qty_gross_net(self):
        for bom_line in self:
            _bomline_qty_net_theorical = self.calculate_qty_net_theoretical(
                bom_line.product_qty, bom_line.loss_percentage
            )
            _diff_product_qty_gross_net = round(
                (bom_line.product_qty_net - _bomline_qty_net_theorical), 2
            )
            bom_line.diff_product_qty_gross_net = _diff_product_qty_gross_net

    # Two buttons to handle two cases : you base your price on net qty or gross qty
    @api.multi
    def set_product_qty_net(self):
        for bom_line in self.filtered(lambda x: x.product_qty):
            bom_line.product_qty_net = self.calculate_qty_net_theoretical(
                bom_line.product_qty, bom_line.loss_percentage
            )

    @api.multi
    def set_product_qty_gross(self):
        for bom_line in self.filtered(lambda x: x.product_qty_net):
            bom_line.product_qty = bom_line.product_qty_net / (
                1 - bom_line.loss_percentage / 100
            )

    # If you change mandatory field product_qty (gross qty), the net quantity adapts
    @api.onchange("product_qty")
    def _onchange_product_qty(self):
        for bom_line in self:
            bom_line.product_qty_net = bom_line.product_qty
