# Copyright (C) 2021-Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.constrains("payment_type")
    def check_payment_type(self):
        if self.payment_type != "inbound" and not self.env.user.has_group(
            "account.group_account_manager"
        ):
            raise ValidationError(
                _("You have no right to select a payment type other than" " inbound.")
            )
