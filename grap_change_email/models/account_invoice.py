# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def action_invoice_sent(self):
        res = super().action_invoice_sent()
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
