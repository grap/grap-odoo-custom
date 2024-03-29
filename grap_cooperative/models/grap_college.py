# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class GrapCollege(models.Model):
    _name = "grap.college"
    _description = "GRAP Colleges"
    _order = "name"

    name = fields.Char("Name", required=True)

    percentage = fields.Integer(string="Percentage", required=True)

    member_ids = fields.One2many(
        string="Members", comodel_name="grap.people", inverse_name="college_id"
    )

    member_qty = fields.Integer(
        string="Members Quantity", compute="_compute_member_qty", store=True
    )

    @api.multi
    @api.depends("member_ids.college_id")
    def _compute_member_qty(self):
        for item in self:
            item.member_qty = len(item.member_ids)
