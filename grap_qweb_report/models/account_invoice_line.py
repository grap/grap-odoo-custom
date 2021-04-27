# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    price_total_displayed = fields.Monetary(
        string="Amount (w / wo taxes)", compute="_compute_price_total_displayed"
    )

    # Useful to have two columns for same field with different name
    # and use column_invisible attributes
    # price_total_displayed2 = fields.Monetary(
    #     string="Amount (w / wo taxes) 2", related="price_total_displayed"
    # )

    # price_unit_include_taxes_line = fields.Boolean(
    #     string="Price Unit (w / wo taxes)", related="invoice_id.price_unit_include_taxes"
    #     )

    def _compute_price_total_displayed(self):
        for line in self:
            print("==================== dans le compute __ line")
            price_include = any(line.mapped("invoice_line_tax_ids.price_include"))
            if price_include:
                line.price_total_displayed = line.price_total
            else:
                line.price_total_displayed = line.price_subtotal

    # To have consistent price unit in PDF
    @api.one
    def _compute_price(self):
        print("============== SURCHARGE")
        super(AccountInvoiceLine, self)._compute_price()
        self._compute_price_total_displayed()
