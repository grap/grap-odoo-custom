# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    external_report_layout_id = fields.Many2one(
        default=lambda x: x._default_external_report_layout_id()
    )

    def _default_external_report_layout_id(self):
        return self.env.ref("web.external_layout_standard").id
