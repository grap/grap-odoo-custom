# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductUom(models.Model):
    _inherit = 'product.uom'

    pricetag_available = fields.Boolean(
        string='Available for Pricetag', help="Check this box if you want"
        " to use this Unit of Mesure to display price per this unit"
        " on pricetags.")
