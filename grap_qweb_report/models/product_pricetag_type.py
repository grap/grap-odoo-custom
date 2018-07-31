# coding: utf-8
# Copyright (C) 2012 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductPricetagType(models.Model):
    _name = 'product.pricetag.type'

    # Column Section
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        default=lambda s: s._default_company_id())

    name = fields.Char(string='Type Name', required=True)

    color = fields.Char(
        string='Color', required=True, size=7,
        help="Color of the Pricetag by default. Format #RRGGBB")

    # Default Section
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id
