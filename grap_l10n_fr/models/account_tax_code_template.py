# coding: utf-8
# Copyright (C) 2018-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountTaxCodeTemplate(models.Model):
    _inherit = 'account.tax.code.template'

    ref_nb = fields.Char(
        "Tax Codes suffix in EBP", size=4,
        help="When exporting Entries to EBP, this suffix will be"
        " appended to the Account Number to make it a new Account.")
