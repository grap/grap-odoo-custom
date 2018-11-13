# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class AccountJournal(Model):
    _inherit = 'account.journal'

    _columns = {
        'move_to_check': fields.boolean(
            string='Moves to Check', help="If you check this box,"
            " account moves created in this journal"
            " will be marked as 'To check by a financial manager'."),
    }
