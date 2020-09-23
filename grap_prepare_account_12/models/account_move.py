# coding: utf-8
# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from openerp import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    tax_state = fields.Selection(
        selection=[
            ("todo", "Todo"),
            ("done", "Done"),
            ("error", "Error"),
        ],
        default="todo",
    )

    @api.model
    def _run_precompute(self, quantity, state, journal_ids):
        _logger.info("Running Pre compute V12 Taxes")
        if not state:
            state = ["todo"]
        domain = [
            ('tax_state', 'in', state),
        ]
        if journal_ids:
            domain += [('journal_id', 'in', journal_ids)]

        moves_for_step_1 = self.search(
            domain, limit=quantity, order="date desc")
        if moves_for_step_1:
            moves_for_step_1.precompute_V12_tax_data()

    @api.multi
    def precompute_V12_tax_data(self):

        def _error(line, done_line_ids):
            line.set_tax_state('error')
            done_line_ids.append(line.id)

        def _finish_move(move, move_qty, tax_state, done_line_ids):
            # Log & Update Move State
            message = "[STEP1] %s/%s - Move '%s' %d - %s" % (
                str(i).zfill(len(str(move_qty))), move_qty,
                tax_state, move.id, str(move.name))
            if tax_state == 'done':
                _logger.info(message)
            else:
                _logger.error(message)

            move.set_tax_state(tax_state)

            # Update Move Line State
            not_concerned_lines = move.mapped("line_id").filtered(
                lambda x: x.id not in done_line_ids)
            not_concerned_lines.set_tax_state('not_concerned')

        AccountTax = self.env["account.tax"]
        InternalUse = self.env["internal.use"]
        move_qty = len(self)
        i = 0

        self.reset_precompute_v12()
        for move in self:
            i += 1
            tax_list = []
            tax_state = 'done'

            done_line_ids = []
            # First, check if it's a move from internal use
            uses = InternalUse.search([('account_move_id', '=', move.id)])
            if uses:
                supplier_taxes = uses.mapped(
                    "line_ids.product_id.supplier_taxes_id")
                for line in move.mapped("line_id").filtered(
                        lambda x: x.tax_code_id):
                    taxes = supplier_taxes.filtered(
                        lambda x: x.base_code_id.id == line.tax_code_id.id)
                    if len(taxes) != 1:
                        tax_state = 'error'
                        _error(line, done_line_ids)
                    else:
                        line.add_tax_ids([taxes[0].id])
                        done_line_ids.append(line.id)
                _finish_move(move, move_qty, tax_state, done_line_ids)
                continue

            # Get main deposit lines, if any
            main_deposit_lines = move.mapped("line_id").filtered(
                lambda x: x.tax_code_id.for_deposit_line)
            if main_deposit_lines:
                for main_deposit_line in main_deposit_lines:
                    taxes = AccountTax.search([
                        ("base_code_id", "=",
                            main_deposit_line.tax_code_id.id),
                        ("account_collected_id", "=",
                            main_deposit_line.account_id.id),
                    ])
                    # Special case for A l'aunée des bois
                    # that changed from assujetti to non assujetti
                    # between 2017 and 2018
                    if len(taxes) == 2\
                            and main_deposit_line.account_id.id == 8574:
                        if move.date >= '2018-01-01':
                            taxes = taxes.filtered(lambda x: x.amount == 0)
                        elif move.date < '2018-01-01':
                            taxes = taxes.filtered(lambda x: x.amount != 0)

                    if len(taxes) != 1:
                        tax_state = 'error'
                        _error(main_deposit_line, done_line_ids)
                        continue
                    main_deposit_line.add_tax_ids([taxes[0].id])
                    done_line_ids.append(main_deposit_line.id)

                    # get related tax line (if exist)
                    related_tax_lines = move.mapped("line_id").filtered(
                        lambda x: x.account_id.id ==
                        main_deposit_line.account_id.id
                        and x.name == taxes[0].name)

                    if len(related_tax_lines) < 1:
                        if taxes[0].amount != 0:
                            tax_state = 'error'
                            _error(main_deposit_line, done_line_ids)
                            continue
                    else:
                        related_tax_lines.set_tax_line_id(taxes[0].id)
                        done_line_ids += related_tax_lines.ids

            # Handle regular sale and purchase
            with_tax_code_lines = move.mapped("line_id").filtered(
                lambda x: x.tax_code_id and x.id not in done_line_ids)
            for line in with_tax_code_lines.filtered(
                    lambda x: x.tax_code_id.for_tax_line):
                # Handle Tax lines
                taxes = AccountTax.with_context(active_test=False).search([
                    ("tax_code_id", "=", line.tax_code_id.id),
                    ("name", "=", line.name)
                ])
                if len(taxes) != 1:
                    tax_state = 'error'
                    _error(line, done_line_ids)
                    continue
                else:
                    line.set_tax_line_id(taxes[0].id)
                    tax_list.append(taxes[0])
                    done_line_ids.append(line.id)

            for line in with_tax_code_lines.filtered(
                    lambda x: x.tax_code_id.for_main_line):
                # Handle Main lines
                taxes = []
                for tax in tax_list:
                    if tax.base_code_id.id == line.tax_code_id.id:
                        taxes.append(tax)
                if len(taxes) == 0:
                    tax_state = 'error'
                    _error(line, done_line_ids)
                    continue
                elif len(taxes) == 1:
                    line.add_tax_ids([taxes[0].id])
                    done_line_ids.append(line.id)
                else:

                    # Petit algorithme bien daubé.
                    # on choppe toutes les lignes de taxes correspondant
                    # au TVA de la ligne en question.
                    # on choisit la ligne la plus grande, en terme de montant
                    taxes_lines = self.env["account.move.line"].search([
                        ('move_id', '=', move.id),
                        ('name', 'in', [x.name for x in taxes]),
                        ('tax_code_id', '=', taxes[0].tax_code_id.id),
                    ], order='tax_amount desc')
                    if len(taxes_lines) == 0:
                        tax_state = 'error'
                        _error(line, done_line_ids)
                        continue
                    else:
                        found_tax = False
                        for tax in taxes:
                            if tax.name == taxes_lines[0].name:
                                found_tax = tax
                        line.add_tax_ids([found_tax.id])
                        done_line_ids.append(line.id)

            _finish_move(move, move_qty, tax_state, done_line_ids)

    @api.multi
    def reset_precompute_v12(self):
        for move in self.filtered(lambda x: x.tax_state != "todo"):
            move.mapped("line_id").remove_tax_ids()
            move.mapped("line_id").set_tax_line_id(False)
            move.set_tax_state("todo")

    @api.multi
    def set_tax_state(self, tax_state):
        self._cr.execute(
            "UPDATE account_move"
            " SET tax_state = %s"
            " WHERE id in %s", (
                tax_state, tuple(self.ids),))
