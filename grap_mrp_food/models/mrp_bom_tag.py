# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBomTag(models.Model):
    _name = "mrp.bom.tag"
    _description = "Bill Of Material Tag"

    # Column Section
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda s: s._default_company_id(),
    )

    name = fields.Char(string="Name", required=True)

    color = fields.Integer("Color Index", default=0)

    bom_ids = fields.Many2many(
        comodel_name="mrp.bom",
        inverse_name="bom_tag_ids",
    )

    bom_qty = fields.Integer(
        string="BoM Quantity", compute="_compute_bom_qty", store=True
    )

    @api.depends("bom_ids")
    def _compute_bom_qty(self):
        for bom_tag in self:
            bom_tag.bom_qty = len(bom_tag.bom_ids)

    # Default Section
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id
