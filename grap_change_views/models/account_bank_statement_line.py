# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'
    _order = 'date desc, journal_id'
