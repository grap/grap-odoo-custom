# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompanyLead(models.Model):
    _name = "res.company.lead"
    _inherit = "res.company"

    stage_id = fields.Many2one(
        "res.company.lead.stage",
        string="Stage",
        ondelete="restrict",
        track_visibility="onchange",
        index=True,
        required=True,
        group_expand="_read_group_stage_ids",
    )

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return stages.browse(stages._search(domain, order=order))
