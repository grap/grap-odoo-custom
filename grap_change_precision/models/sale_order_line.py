# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin = fields.Float(
        digits=dp.get_precision("GRAP Cost Price")
    )

    purchase_price = fields.Float(
        digits=dp.get_precision("GRAP Cost Price")
    )
