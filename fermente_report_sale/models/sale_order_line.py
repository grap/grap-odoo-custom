# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        values = super()._prepare_invoice_line(**optional_values)

        if self.env.context.get("add_picking_date", False) and self.move_ids:
            prefix = (
                self.move_ids[0].date
                and self.move_ids[0].date.strftime("%Y-%m-%d") + " - "
                or ""
            )
            values["name"] = prefix + values["name"]
        return values
