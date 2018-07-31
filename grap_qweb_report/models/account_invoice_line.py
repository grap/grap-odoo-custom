# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models

import openerp.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    price_unit_vat_excluded = fields.Float(
        compute='_compute_price_unit_vat_excluded',
        digits_compute=dp.get_precision('Purchase Price'))

    @api.multi
    def _compute_price_unit_vat_excluded(self):
        for line in self:
            tmp = line.invoice_line_tax_id.compute_all(
                line.price_unit, line.quantity, line.product_id,
                line.invoice_id.partner_id)
            line.price_unit_vat_excluded = (
                tmp['taxes'] and tmp['taxes'][0]['price_unit'] or
                line.price_unit)
