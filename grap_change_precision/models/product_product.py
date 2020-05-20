# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.addons import decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = "product.product"

    volume = fields.Float(
        digits=dp.get_precision("GRAP Stock Volume")
    )

    standard_price = fields.Float(
        digits=dp.get_precision("GRAP Cost Price")
    )

    standard_price_tax_included = fields.Float(
        digits=dp.get_precision("GRAP Cost Price")
    )
