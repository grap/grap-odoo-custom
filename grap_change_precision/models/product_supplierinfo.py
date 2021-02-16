# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

from odoo.addons import decimal_precision as dp


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    price = fields.Float(
        digits=dp.get_precision("GRAP Supplierinfo Price")
    )
