# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_sent(self):
        """Return the custom GRAP template"""
        res = super(AccountInvoice, self).action_invoice_sent()
        template = self.env.ref(
            "grap_change_email.email_template_account_invoice"
        )
        res["context"].update(
            {
                "default_use_template": bool(template.id),
                "default_template_id": template.id,
            }
        )
        return res
