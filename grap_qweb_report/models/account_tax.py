# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    report_short_code = fields.Char(compute='_compute_report_short_code')

    @api.multi
    def _compute_report_short_code(self):
        for tax in self:
            tax.report_short_code = "%s%%" % (
                str(tax.amount * 100).replace('.', ','))
