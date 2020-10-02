# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    price_total_displayed = fields.Monetary(
        string="Amount (w / wo taxes)",
        compute="_compute_price_total_displayed")

    def _compute_price_total_displayed(self):
        for line in self:
            price_include = any(line.mapped(
                "invoice_line_tax_ids.price_include"))
            if price_include:
                line.price_total_displayed = line.price_total
            else:
                line.price_total_displayed = line.price_subtotal
