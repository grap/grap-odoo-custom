# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    categ_id = fields.Many2one(default=lambda x: x._default_categ_id())

    type = fields.Selection(default="product")

    def _default_categ_id(self):
        if self.env.context.get("joint_buying", False):
            return self._get_default_category_id()
        return False
