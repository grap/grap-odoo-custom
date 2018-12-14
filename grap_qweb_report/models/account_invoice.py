# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models

import openerp.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    has_discount = fields.Boolean(compute='_compute_has_discount')
    extra_costs = fields.Float(
        compute='_compute_extra_costs',
        digits_compute=dp.get_precision('Purchase Price'))

    @api.multi
    def _compute_has_discount(self):
        for invoice in self:
            invoice.has_discount = len(
                invoice.invoice_line.filtered(lambda x: x.discount))

    @api.multi
    def _compute_extra_costs(self):
        for invoice in self:
            for product in invoice.invoice_line:
                if product.product_id.invoice_extra_cost:
                    invoice.extra_costs += product.price_subtotal
