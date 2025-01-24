# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    categ_id = fields.Many2one(default=lambda x: x._get_default_category_id())

    def _get_default_category_id(self):
        if not self.env.ref("product.product_category_all").active:
            return False
        return super()._get_default_category_id()
