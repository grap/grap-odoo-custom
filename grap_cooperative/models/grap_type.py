# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class GrapType(models.Model):
    _name = "grap.type"
    _description = "GRAP Activity Types"

    name = fields.Char(string="Name", required=True)

    activity_ids = fields.One2many(
        string="Activities",
        comodel_name="grap.activity",
        inverse_name="type_id",
    )

    activity_qty = fields.Integer(
        string="Activities Quantity",
        compute="_compute_activity_qty",
        store=True,
    )

    @api.depends("activity_ids.type_id")
    def _compute_activity_qty(self):
        for item in self:
            item.activity_qty = len(item.activity_ids)
