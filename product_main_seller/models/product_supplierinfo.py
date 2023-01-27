# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    is_main_seller = fields.Boolean(compute="_compute_is_main_seller")
    is_main_seller_icon = fields.Char(default="🥇")

    @api.depends("sequence")
    def _compute_is_main_seller(self):
        for supplierinfo in self:
            supplierinfo.is_main_seller = supplierinfo.sequence == 1
