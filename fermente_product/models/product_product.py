# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    standard_price = fields.Float(copy=True, tracking=True)

    lst_price = fields.Float(tracking=True)
