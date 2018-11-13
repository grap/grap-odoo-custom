# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model


class AccountMove(Model):
    _inherit = 'account.move'

    def create(self, cr, uid, vals, context=None):
        journal_obj = self.pool['account.journal']
        if vals.get('journal_id', False) and not vals.get('to_check'):
            journal = journal_obj.browse(
                cr, uid, vals['journal_id'], context=context)
            vals['to_check'] = journal.move_to_check
        return super(AccountMove, self).create(cr, uid, vals, context=context)
