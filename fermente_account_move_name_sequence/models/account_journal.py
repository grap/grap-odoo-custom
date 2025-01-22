# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    sequence_prefix = fields.Char(
        string="Sequence Prefix", related="sequence_id.prefix"
    )

    refund_sequence_prefix = fields.Char(
        string="Refund Sequence Prefix", related="refund_sequence_id.prefix"
    )
