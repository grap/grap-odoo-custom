# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_invoice_create(self, grouped=False, final=False):
        if not grouped and len(self) > 1:
            return super(SaleOrder, self.with_context(
                add_picking_date=True)).action_invoice_create(
                    grouped=grouped, final=final)
        return super().action_invoice_create(grouped=grouped, final=final)
