# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    post_at_bank_rec_journal = fields.Boolean(related="journal_id.post_at_bank_rec")

    @api.multi
    def action_post_no_check(self):
        self.post()
