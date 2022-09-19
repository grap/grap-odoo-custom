# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # ======== TIME
    time_to_produce_per_unit = fields.Float(
        string="Theorical time per unit",
        related="product_id.time_to_produce_product",
    )
    time_to_produce_line = fields.Float(
        string="Real time",
    )
    time_to_produce_line_theorical = fields.Float(
        string="Theorical time",
    )
    diff_time_product_theorical = fields.Float(
        string="Diff Time",
    )

    @api.onchange("product_id", "time_to_produce_per_unit", "product_qty")
    def _onchange_time_to_produce_line(self):
        self.time_to_produce_line = self.time_to_produce_per_unit * self.product_qty
        self.time_to_produce_line_theorical = self.time_to_produce_line

    # TODO : faire un notify user quand on change dans le product la quantité ?
    # ou mieux, écire en dessous les fiches qui seront impactés ? ou osef ?

    @api.onchange(
        "time_to_produce_per_unit",
        "time_to_produce_line",
        "time_to_produce_line_theorical",
    )
    def _onchange_diff_time_product_theorical(self):
        self.diff_time_product_theorical = (
            self.time_to_produce_line - self.time_to_produce_line_theorical
        )

    @api.multi
    def set_time_product_theorical(self):
        for bomline in self:
            bomline.time_to_produce_line = bomline.time_to_produce_line_theorical
            bomline.diff_time_product_theorical = 0
