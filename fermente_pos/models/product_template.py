# Copyright (C) 2026-Today: GRAP (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    available_in_pos = fields.Boolean(default=lambda x: x._default_available_in_pos())

    @api.model
    def _default_available_in_pos(self):
        return not self.env.context.get("joint_buying")
