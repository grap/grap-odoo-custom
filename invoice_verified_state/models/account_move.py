# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        AccountJournal = self.env['account.journal']
        if vals.get('journal_id', False) and not vals.get('to_check'):
            journal = AccountJournal.browse(
                vals['journal_id'])
            vals['to_check'] = journal.move_to_check
        return super(AccountMove, self).create(vals)
