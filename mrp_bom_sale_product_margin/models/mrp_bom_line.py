# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # New fields
    standard_price_unit = fields.Float(compute="_compute_standard_price_unit")
    currency_id = fields.Many2one(related="product_id.currency_id")

    standard_price_subtotal = fields.Float(
        string="Subtotal price", compute="_compute_standard_price_subtotal"
    )

    @api.multi
    @api.depends("standard_price_unit", "product_qty")
    def _compute_standard_price_subtotal(self):
        for line in self:
            line.standard_price_subtotal = line.standard_price_unit * line.product_qty

    @api.multi
    @api.depends("product_id")
    def _compute_standard_price_unit(self):
        for line in self:
            line.standard_price_unit = line.product_id.standard_price
