# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class GrapCategory(models.Model):
    _name = "grap.category"
    _description = "GRAP Activity Categories"

    name = fields.Char("Name", required=True)

    activity_ids = fields.Many2many(
        string="Activities",
        comodel_name="grap.activity",
        relation="grap_activity_category_rel",
        column1="category_id",
        column2="activity_id",
    )

    activity_qty = fields.Integer(
        string="Activities Quantity", compute="_compute_activity_qty", store=True
    )

    color = fields.Integer(string="Color Index")

    @api.multi
    @api.depends("activity_ids")
    def _compute_activity_qty(self):
        for item in self:
            item.activity_qty = len(item.activity_ids)
