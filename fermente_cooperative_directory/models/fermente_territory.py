# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FermenteTerritory(models.Model):
    _name = "fermente.territory"
    _description = "Fermente custom Territory"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        required=True,
    )

    company_ids = fields.One2many(
        string="Companies in this Territory",
        comodel_name="res.company",
        inverse_name="territory_id",
    )

    company_qty = fields.Integer(
        string="Companies Quantity",
        compute="_compute_company_qty",
        store=True,
        recursive=True,
    )

    @api.depends(
        "company_ids.territory_id",
        "company_ids.is_displayed_in_directory",
        "company_ids.active",
    )
    def _compute_company_qty(self):
        for territory in self:
            territory.company_qty = len(
                territory.company_ids.filtered(
                    lambda x: x.active and x.is_displayed_in_directory
                )
            )
