# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Column Section
    tax_ids_description = fields.Char(
        string='Taxes', compute='_compute_tax_ids_description',
        store=True)

    # Compute Section
    @api.multi
    @api.depends('taxes_id')
    def _compute_tax_ids_description(self):
        for line in self:
            line.tax_ids_description = ','.join(
                [x.description and x.description or x.name
                    for x in line.taxes_id])
