# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompanyLeadStage(models.Model):
    _name = "res.company.lead.stage"
    _description = "Company Leads Stages"
    _rec_name = "name"
    _order = "sequence, name, id"

    name = fields.Char("Stage Name", required=True, translate=True)

    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )

    fold = fields.Boolean(
        "Folded in Pipeline",
        help="This stage is folded in the kanban view when"
        " there are no records in that stage to display.",
    )

    description = fields.Text(
        "Description",
        help="Enter here the internal requirements for this stage."
        " It will appear as a tooltip over the stage's name.",
    )

    lead_qty = fields.Integer("Leads Quantity", compute="_compute_lead_qty", store=True)

    lead_ids = fields.One2many(comodel_name="res.company.lead", inverse_name="stage_id")

    @api.multi
    def _compute_lead_qty(self):
        for stage in self:
            stage.team_count = len(stage.lead_ids)
