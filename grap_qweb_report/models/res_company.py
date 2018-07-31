# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    pricetag_color = fields.Char(
        'Pricetag Color', required=True, size=7, default='#FFFFFF',
        help="Color of the Pricetag by default. Format #RRGGBB")

    pricetag_ignore_organic_warning = fields.Boolean(
        string='Ignore Organic Warning', help="Check this box if you want"
        " to hide the mention 'Not From Organic Farming' that is displayed"
        " on pricetags for foods products that don't have an organic label")
