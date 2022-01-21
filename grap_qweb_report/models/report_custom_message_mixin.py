# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.osv import expression


class ReportCustomMessageMixin(models.AbstractModel):
    _description = "Report Custom Message Mixin"
    _name = "report.custom.message.mixin"

    report_custom_message = fields.Text(compute="_compute_report_custom_message")

    @api.multi
    def _compute_report_custom_message(self):
        ReportCustomMessage = self.env["report.custom.message"]
        for item in self:
            domain = expression.OR(
                [
                    [("company_id", "=", False)],
                    [("company_id", "child_of", [item.company_id.id])],
                ]
            )
            if self._name == "account.invoice":
                model_domain = ("display_on_account_invoice", "=", True)
            elif self._name == "purchase.order":
                model_domain = ("display_on_purchase_order", "=", True)
            elif self._name == "sale.order":
                model_domain = ("display_on_sale_order", "=", True)
            elif self._name == "stock.picking":
                model_domain = ("display_on_stock_picking", "=", True)

            domain = expression.AND([domain, [model_domain]])
            messages = ReportCustomMessage.search(domain)
            item.report_custom_message = "".join(messages.mapped("message"))
