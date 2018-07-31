# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_invoice_create(
            self, journal_id, group=False, type='out_invoice'):
        return super(StockPicking, self.with_context(
            add_picking_date=group)).action_invoice_create(
                journal_id, group=group, type=type)
