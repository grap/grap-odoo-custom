# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # Column Section
    date_planned = fields.Datetime(compute=False)

    state = fields.Selection(selection_add=[("done", "Archived")])

    def button_confirm(self):
        self.action_set_date_planned()
        return super().button_confirm()
