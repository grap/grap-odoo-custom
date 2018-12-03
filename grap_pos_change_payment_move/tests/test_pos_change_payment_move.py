# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from openerp.tests.common import TransactionCase


class TetsChangePaymentMove(TransactionCase):

    def setUp(self):
        super(TetsChangePaymentMove, self).setUp()

        self.session_obj = self.env['pos.session']
        self.order_obj = self.env['pos.order']
        self.move_obj = self.env['account.move']

        self.pos_config = self.env.ref('point_of_sale.pos_config_main')
        self.product_evian = self.env.ref('point_of_sale.evian_2l')
        self.partner_agrolait = self.env.ref('base.res_partner_2')
        self.cash_journal = self.env.ref('account.cash_journal')

    # Tools function section
    def _open_session(self):
        return self.session_obj.create({'config_id': self.pos_config.id})

    def _sale(self, session, partner, journal, qty, date_diff=0):
        order = self.order_obj.create({
            'session_id': session.id,
            'partner_id': partner and partner.id or False,
            'lines': [[0, False, {
                'discount': 0,
                'price_unit': 1,
                'product_id': self.product_evian.id,
                'qty': qty}]]
        })
        if date_diff:
            order.date_order =\
                datetime.strptime(order.date_order, "%Y-%m-%d %H:%M:%S") +\
                timedelta(days=date_diff)
        self.order_obj.add_payment(
            order.id, {'amount': qty, 'journal': journal.id})

        order.signal_workflow('paid')
        return order

    def _close_session(self, session):
        session.signal_workflow('close')

    def _get_payment_move(self, session, journal, partner_id):
        return self.move_obj.search([
            ('ref', '=', session.name),
            ('journal_id', '=', journal.id),
            ('partner_id', '=', partner_id)])

    def _get_first_move_line(self, move, is_debit):
        self.assertEquals(
            len(move.line_id), 2,
            "Payment moves from Point of Sale should have two lines.")
        if move.line_id[0].debit and is_debit:
            return move.line_id[0]
        else:
            return move.line_id[1]

    # Test Section
    def test_01_test_many_uninvoiced_orders(self):
        """Test if making many PoS orders uninvoiced generated a single
            good accounting entry.
        """
        session = self._open_session()
        # anonymous sale
        self._sale(session, False, self.cash_journal, 50)
        # Anonymous return
        self._sale(session, False, self.cash_journal, -10)
        # sale #1 with customer, without invoice
        self._sale(session, self.partner_agrolait, self.cash_journal, 20)
        # sale #2 with customer, without invoice
        self._sale(session, self.partner_agrolait, self.cash_journal, 40)

        self._close_session(session)

        payment_moves = self._get_payment_move(
            session, self.cash_journal, False)

        self.assertEquals(
            len(payment_moves), 1,
            "Anonymous PoS orders (or uninvoiced PoS Orders) should generate"
            " a uniq payment move when closing the session")

        bank_line = self._get_first_move_line(payment_moves[0], True)
        self.assertEquals(
            bank_line.debit, 100,
            "incorrect Debit value for 4 sales (50, -10, 20, 40)")

    # Test Section
    def test_02_test_invoiced_orders(self):
        """Test if making many PoS orders invoiced generated a single
            good accounting entry.
        """
        session = self._open_session()
        # sale #1 with customer, without invoice
        self._sale(session, self.partner_agrolait, self.cash_journal, 1)
        # sale #2 with customer, without invoice
        self._sale(session, self.partner_agrolait, self.cash_journal, 10)

        # sale #3 with customer, with invoice
        order = self._sale(
            session, self.partner_agrolait, self.cash_journal, 20)
        order.action_invoice()
        # sale #4 with customer, with invoice
        order = self._sale(
            session, self.partner_agrolait, self.cash_journal, 40)
        order.action_invoice()

        self._close_session(session)

        anonymous_payment_moves = self._get_payment_move(
            session, self.cash_journal, False)

        customer_payment_moves = self._get_payment_move(
            session, self.cash_journal, self.partner_agrolait.id)

        self.assertEquals(
            len(anonymous_payment_moves), 1,
            "orders of a given partner, invoiced and not invoiced, should"
            " generate an anonymous move and one with customer.")

        self.assertEquals(
            len(customer_payment_moves), 1,
            "orders of a given partner, invoiced and not invoiced, should"
            " generate an anonymous move and one with customer.")

        bank_line = self._get_first_move_line(anonymous_payment_moves[0], True)
        self.assertEquals(
            bank_line.debit, 11,
            "incorrect Debit value for 2 uninvoiced orders (1, 11)")

        bank_line = self._get_first_move_line(customer_payment_moves[0], True)
        self.assertEquals(
            bank_line.debit, 60,
            "incorrect Debit value for 2 invoiced orders (20, 40)")

    # Test Section
    def test_03_move_per_day(self):
        """Test if making many PoS orders invoiced generated a single
            good accounting entry.
        """
        session = self._open_session()
        # sale #1 date 1
        self._sale(session, False, self.cash_journal, 10)
        # sale #2 date 2
        self._sale(session, False, self.cash_journal, 20, date_diff=1)
        self._close_session(session)

        anonymous_payment_moves = self._get_payment_move(
            session, self.cash_journal, False)

        self.assertEquals(
            len(anonymous_payment_moves), 2,
            "Closing session should generate 1 payment move per day.")
