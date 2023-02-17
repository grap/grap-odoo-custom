# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    packaging = fields.Many2one(
        comodel_name="product.product", domain="[('is_packaging', '=', True)]"
    )
    packaging_name = fields.Char(
        related="packaging.name",
        string="Packaging",
    )
    packaging_on_bom_lines = fields.Boolean(compute="_compute_packaging_on_bom_lines")

    @api.multi
    @api.depends("packaging", "bom_line_ids")
    def _compute_packaging_on_bom_lines(self):
        for bom in self:
            bom_lines = bom.bom_line_ids.filtered(
                lambda x: x.product_id == bom.packaging
            )
            bom.packaging_on_bom_lines = bool(bom_lines)

    @api.multi
    def add_packaging_to_bom_lines(self):
        self.ensure_one()
        self.bom_line_ids.create(
            {
                "product_id": self.packaging.id,
                "bom_id": self.id,
                "sequence": 1000,
            }
        )
