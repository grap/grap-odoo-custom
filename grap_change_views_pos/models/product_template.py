# Copyright (C) 2018-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    available_in_pos = fields.Boolean(default=lambda x: x._default_available_in_pos())

    def _default_available_in_pos(self):
        return not self.env.context.get("joint_buying")
