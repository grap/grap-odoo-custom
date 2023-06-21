# Copyright (C) 2023-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductPricelistPrint(models.TransientModel):
    _inherit = "product.pricelist.print"

    show_eshop_rounded_qty = fields.Boolean(string="Show Packaging")
