# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _get_aml_default_display_name_list(self):
        self.ensure_one()
        values = [("label", self.ref)]

        if self.partner_id:
            values += [
                ("sep", " - "),
                ("partner", self.partner_id.display_name),
            ]
        return values
