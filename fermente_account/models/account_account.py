# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.model
    def _get_most_frequent_accounts_for_partner(
        self,
        company_id,
        partner_id,
        move_type,
        filter_never_user_accounts=False,
        limit=None,
    ):
        return []
