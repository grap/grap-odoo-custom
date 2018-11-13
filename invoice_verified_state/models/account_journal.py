# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    move_to_check = fields.Boolean(
        string='Moves to Check', help="If you check this box,"
        " account moves created in this journal"
        " will be marked as 'To check by a financial manager'.")
