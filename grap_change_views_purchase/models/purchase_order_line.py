# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.model
    def _get_date_planned(self, seller, po=False):
        # Overwrite this function the date_planned of the lines are
        # the date planned of the order, otherwise, the date of the order.
        order = po if po else self.order_id
        return order.date_planned or order.date_order
