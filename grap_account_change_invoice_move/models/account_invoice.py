# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def inv_line_characteristic_hashcode(self, invoice_line):
        """
        We override this function to group lines regardless of the product_id.
        Lines having the same hashcode will be grouped together if the journal
        has the 'group line' option. """
        return "%s-%s-%s-%s" % (
            invoice_line["account_id"],
            invoice_line.get("tax_code_id", "False"),
            invoice_line.get("analytic_account_id", "False"),
            invoice_line.get("date_maturity", "False"),
        )
