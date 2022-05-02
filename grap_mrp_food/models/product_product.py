# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    date_last_statement_price = fields.Date(string="Date Last Statement Price")

    @api.onchange("standard_price")
    def _onchange_date_last_statement_price(self):
        for product in self:
            product.date_last_statement_price = fields.Date.today()
