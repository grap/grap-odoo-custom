# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # Column Section
    line_qty_percentage = fields.Float(
        string="Qty %", compute="_compute_line_qty_percentage", store=True
    )

    @api.depends("product_qty", "bom_id.bom_line_ids.product_qty")
    def _compute_line_qty_percentage(self):
        for line in self:
            total_qty = sum(line.bom_id.bom_line_ids.mapped("product_qty"))
            line.line_qty_percentage = line.product_qty / total_qty
