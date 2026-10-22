# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


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
