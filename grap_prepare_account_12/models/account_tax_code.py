# coding: utf-8
# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountTaxCode(models.Model):
    _inherit = 'account.tax.code'

    for_main_line = fields.Boolean(default=False, readonly=True)

    for_tax_line = fields.Boolean(default=False, readonly=True)

    for_deposit_line = fields.Boolean(default=False, readonly=True)
