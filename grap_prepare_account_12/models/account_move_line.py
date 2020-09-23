# coding: utf-8
# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    tax_ids = fields.Many2many(
        comodel_name='account.tax',
        string='Taxes Applied',
        help="Taxes that apply on the base amount")

    tax_line_id = fields.Many2one(
        comodel_name='account.tax',
        string='Originator tax',
        help="Indicates that this journal item is a tax line")

    tax_state = fields.Selection(
        selection=[
            ("todo", "Todo"),
            ("not_concerned", "Not concerned"),
            ("done", "Done"),
            ("error", "Error"),
        ],
        default="todo",
    )

    @api.multi
    def add_tax_ids(self, tax_ids):
        self.ensure_one()
        for tax_id in tax_ids:
            self._cr.execute(
                "INSERT INTO account_move_line_account_tax_rel"
                " (account_move_line_id, account_tax_id)"
                " VALUES (%s, %s)", (self.id, tax_id))
        self.set_tax_state('done')

    @api.multi
    def remove_tax_ids(self):
        self.set_tax_state('todo')
        if not self.ids:
            return
        self._cr.execute(
            "DELETE FROM account_move_line_account_tax_rel"
            " WHERE account_move_line_id in %s", (
                tuple(self.ids),))

    @api.multi
    def set_tax_line_id(self, tax_id):
        if tax_id:
            self._cr.execute(
                "UPDATE account_move_line"
                " SET tax_line_id = %s,"
                " tax_state = 'done'"
                " WHERE id in %s", (
                    tax_id, tuple(self.ids),))
        else:
            self._cr.execute(
                "UPDATE account_move_line"
                " SET tax_line_id = null,"
                " tax_state = 'todo'"
                " WHERE id in %s", (
                    tuple(self.ids),))

    @api.multi
    def set_tax_state(self, tax_state):
        if not self.ids:
            return
        self._cr.execute(
            "UPDATE account_move_line"
            " SET tax_state = %s"
            " WHERE id in %s", (
                tax_state, tuple(self.ids),))
