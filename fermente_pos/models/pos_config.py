# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    account_default_pos_receivable_account_id = fields.Many2one(
        string="Default Account Receivable (PoS)",
        related="company_id.account_default_pos_receivable_account_id",
        readonly=False,
        required=True,
    )

    def _default_sale_journal(self):
        return self._default_invoice_journal()

    def _check_header_footer(self, values):
        return True
