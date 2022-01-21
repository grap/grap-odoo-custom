# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res.update(
            {
                "template_id": self.env.ref(
                    "grap_change_email.email_template_account_invoice"
                ).id,
            }
        )
        return res
