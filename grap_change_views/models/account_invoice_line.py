# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # Column Section
    type = fields.Selection(
        related='invoice_id.type', string='Type', select=True, store=True,
        readonly=True)

    state = fields.Selection(
        related='invoice_id.state', string='State', select=True, store=True,
        readonly=True)

    partner_id = fields.Many2one(
        related='invoice_id.partner_id', string='Partner',
        comodel_name='res.partner', select=True, store=True, readonly=True)

    date_invoice = fields.Date(
        related='invoice_id.date_invoice', string='Date invoice', select=True,
        store=True, readonly=True)

    categ_id = fields.Many2one(
        related='product_id.categ_id', string='Category', select=True,
        comodel_name='product.category', store=True, readonly=True)

    tax_ids_description = fields.Char(
        string='Taxes', compute='_compute_tax_ids_description',
        store=True)

    # Compute Section
    @api.multi
    @api.depends('invoice_line_tax_id')
    def _compute_tax_ids_description(self):
        for line in self:
            line.tax_ids_description = ','.join(
                [x.description and x.description or x.name
                    for x in line.invoice_line_tax_id])
