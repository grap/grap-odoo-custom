# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from openerp.tests.common import TransactionCase


class TestChangeSaleMove(TransactionCase):

    def setUp(self):
        super(TestChangeSaleMove, self).setUp()

        self.session_obj = self.env['pos.session']
        self.order_obj = self.env['pos.order']
        self.move_obj = self.env['account.move']
        self.move_line_obj = self.env['account.move.line']

        self.pos_config = self.env.ref('point_of_sale.pos_config_main')
        self.product_no_vat = self.env.ref(
            'grap_pos_change_sale_move.product_no_vat')
        self.product_vat_5_707 = self.env.ref(
            'grap_pos_change_sale_move.product_5_707')
        self.product_vat_20_701 = self.env.ref(
            'grap_pos_change_sale_move.product_20_701')
        self.product_vat_20_707 = self.env.ref(
            'grap_pos_change_sale_move.product_20_707')
        self.partner_agrolait = self.env.ref('base.res_partner_2')
        self.sale_journal = self.env.ref('account.sales_journal')
        self.cash_journal = self.env.ref('account.cash_journal')
        self.partner_account = self.env.ref('account.a_recv')
        self.account_vat_5 = self.env.ref(
            'grap_pos_change_sale_move.account_vat_5')
        self.account_vat_20 = self.env.ref(
            'grap_pos_change_sale_move.account_vat_20')
        self.account_income_701 = self.env.ref(
            'grap_pos_change_sale_move.account_income_701')
        self.account_income_707 = self.env.ref(
            'grap_pos_change_sale_move.account_income_707')
        self.tax_code_base_5 = self.env.ref(
            'grap_pos_change_sale_move.tax_code_base_5')
        self.tax_code_5 = self.env.ref(
            'grap_pos_change_sale_move.tax_code_5')
        self.tax_code_base_20 = self.env.ref(
            'grap_pos_change_sale_move.tax_code_base_20')
        self.tax_code_20 = self.env.ref(
            'grap_pos_change_sale_move.tax_code_20')

    # Tools function section
    def _open_session(self):
        return self.session_obj.create({'config_id': self.pos_config.id})

    def _sale(self, session, partner, product, qty, date_diff=0):
        order = self.order_obj.create({
            'session_id': session.id,
            'partner_id': partner and partner.id or False,
            'lines': [[0, False, {
                'discount': 0,
                'price_unit': 1,
                'product_id': product.id,
                'tax_ids': product.taxes_id.ids and
                [[6, False, product.taxes_id.ids]] or False,
                'qty': qty}]]
        })
        if date_diff:
            order.date_order =\
                datetime.strptime(order.date_order, "%Y-%m-%d %H:%M:%S") +\
                timedelta(days=date_diff)
        self.order_obj.add_payment(
            order.id, {'amount': qty, 'journal': self.cash_journal.id})

        order.signal_workflow('paid')
        return order

    def _close_session(self, session):
        session.signal_workflow('close')

    def _get_sale_moves(self, session):
        if session:
            return self.move_obj.search([
                ('ref', '=', session.name),
                ('journal_id', '=', self.sale_journal.id)],
                order='date')
        else:
            return self.move_obj.search([
                ('journal_id', '=', self.sale_journal.id)],
                order='date')

    def _get_move_line(self, move, account, tax_code=False):
        res = self.move_line_obj.search([
            ('move_id', '=', move.id),
            ('account_id', '=', account.id),
            ('tax_code_id', '=', tax_code and tax_code.id or False)])

        self.assertEquals(
            len(res), 1, "Expected on single line.")
        return res

    # Test Section
    def test_01_move_per_day(self):
        """Test if making many PoS orders in different days, generate
        an entry per day"""
        session = self._open_session()
        sale_entries_before = len(self._get_sale_moves(False))

        # sale #1 date 1
        self._sale(session, False, self.product_no_vat, 10)
        # sale #1 date 1
        self._sale(session, False, self.product_no_vat, 40)
        # sale #2 date 2
        self._sale(
            session, False, self.product_no_vat, 20,
            date_diff=1)

        self._close_session(session)

        sale_entries_after = len(self._get_sale_moves(False))

        self.assertEquals(
            sale_entries_before + 2, sale_entries_after,
            "Closing session with order on two days should generate 2 sale"
            " entries.")

    def test_02_test_account_and_vat(self):
        """Sale many orders and check result
        """
        session = self._open_session()

        # sale #1 product VAT 5% / Account 707 (210 VAT Excl)
        self._sale(session, False, self.product_vat_5_707, 220.5)
        # sale #2 product VAT 5% / Account 707 (return) (70 VAT Excl)
        self._sale(session, False, self.product_vat_5_707, -73.5)
        # sale #3 product VAT 20% / Account 701 (80 VAT Excl)
        self._sale(session, False, self.product_vat_20_701, 96)
        # sale #4 product VAT 20% / Account 707 (160 VAT Excl)
        self._sale(session, False, self.product_vat_20_707, 192)
        # sale #5 product no VAT / Account 707 (1000 VAT Excl) with customer
        self._sale(session, self.partner_agrolait, self.product_no_vat, 1000)
        # sale #6 product no VAT / Account 707 (1000 VAT Excl) invoiced
        order = self._sale(
            session, self.partner_agrolait, self.product_no_vat, 10000)
        order.action_invoice()

        self._close_session(session)

        sale_moves = self._get_sale_moves(session)
        self.assertEquals(
            len(sale_moves), 1,
            "Anonymous PoS orders (or uninvoiced PoS Orders) should generate"
            " a uniq sale move when closing the session")
        sale_move = sale_moves[0]

        # Check Line quantity
        self.assertEquals(
            len(sale_move.line_id), 7,
            "Incorrect quantity of lines.")

        # Check Customer Line
        line = self._get_move_line(sale_move, self.partner_account)
        self.assertEquals(
            line.debit, 1435.0,
            "incorrect Debit value for customer sales.")

        # Check VAT Line (5%)
        line = self._get_move_line(
            sale_move, self.account_vat_5, self.tax_code_5)
        self.assertEquals(
            line.credit, 7,
            "incorrect Credit value for VAT line (5%).")

        # Check VAT Line (20%)
        line = self._get_move_line(
            sale_move, self.account_vat_20, self.tax_code_20)
        self.assertEquals(
            line.credit, 48,
            "incorrect Credit value for VAT line (20%).")

        # Check Income Line 707 (no vat)
        line = self._get_move_line(sale_move, self.account_income_707)
        self.assertEquals(
            line.credit, 1000,
            "incorrect Credit value for Income 707 line (No VAT).")

        # Check Income Line 707(5%)
        line = self._get_move_line(
            sale_move, self.account_income_707, self.tax_code_base_5)
        self.assertEquals(
            line.credit, 140,
            "incorrect Credit value for Income 707 line (5%).")

        # Check Income Line 707(20%)
        line = self._get_move_line(
            sale_move, self.account_income_707, self.tax_code_base_20)
        self.assertEquals(
            line.credit, 160,
            "incorrect Credit value for Income 707 line (20%).")

        # Check Income Line 701(20%)
        line = self._get_move_line(
            sale_move, self.account_income_701, self.tax_code_base_20)
        self.assertEquals(
            line.credit, 80,
            "incorrect Credit value for Income 701 line (20%).")

        # Check the state of the account move
        self.assertEquals(
            sale_move.state, 'posted', "Sale Move should be posted")
