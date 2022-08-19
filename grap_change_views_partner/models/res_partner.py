# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_account_position_id = fields.Many2one(track_visibility="always")

    # Useful for accessing product in inline tree views
    def see_current_partner(self):
        self.ensure_one()
        result = self.env.ref("base.action_partner_form").read()[0]
        form_view = self.env.ref("base.view_partner_form")
        result["views"] = [(form_view.id, "form")]
        result["res_id"] = self.id
        result["context"] = {
            "form_view_initial_mode": "edit",
        }
        return result
