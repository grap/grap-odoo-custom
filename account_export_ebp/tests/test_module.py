# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.WizardEbpExport = self.env['wizard.ebp.export']
        self.WizardResPartnerAddSuffix = self.env[
            'wizard.res.partner.add.suffix']
        self.move_invoice = self.env.ref('account.invoice_1').move_id
        self.move_1 = self.env.ref('account_export_ebp.move_1')
        self.sale_account = self.env.ref('account.a_sale')
        self.receivable_account = self.env.ref('account.a_recv')

    # Test Section
    def test_01_export_move_correct(self):
        # Add EBP suffix to partner
        suffix_wizard = self.WizardResPartnerAddSuffix.with_context(
            active_ids=[self.move_invoice.partner_id.id]).create({})
        suffix_wizard.button_affect_suffix()

        wizard = self.WizardEbpExport.with_context(
            active_ids=[self.move_invoice.id]).create({})

        wizard.button_export()

        self.assertEqual(
            self.move_invoice.ebp_export_id.id, wizard.ebp_export_id.id,
            "Exporting a move should link it to the ebp export created.")

    def test_02_export_move_without_partner_code(self):
        wizard = self.WizardEbpExport.with_context(
            active_ids=[self.move_invoice.id]).create({})

        wizard.button_export()

        self.assertEqual(
            self.move_invoice.ebp_export_id.id, False,
            "Exporting a move with partner without suffix"
            " should not link it to the ebp export created.")

    def test_02_export_content(self):
        self.move_1.button_validate()

        wizard = self.WizardEbpExport.with_context(
            active_ids=[self.move_1.id]).create({})

        wizard.button_export()
        data_lines = self._get_lines_from_data_move(
            self.move_1.ebp_export_id.data_moves)
        self._asset_line_content(
            data_lines, self.move_1.journal_id.ebp_code,
            self.sale_account.code, 100, 0)
        self._asset_line_content(
            data_lines, self.move_1.journal_id.ebp_code,
            self.sale_account.code, 0, 20)
        self._asset_line_content(
            data_lines, self.move_1.journal_id.ebp_code,
            self.receivable_account.code, 0, 80)

    def _get_lines_from_data_move(self, base64_data):
        datas = base64.decodestring(base64_data)
        data_list = datas.split('\r\n')
        if data_list[0][:4] == 'Line':
            del data_list[0]
        if data_list[-1] == '':
            del data_list[-1]
        return data_list

    def _asset_line_content(
            self, data_lines, journal_code, account_code, debit=0, credit=0):
        matches = []
        for data_line in data_lines:
            ok = True
            line_table = data_line.split(',')
            ok = ok and line_table[2] == journal_code
            ok = ok and line_table[3] == account_code
            if credit:
                ok = ok and line_table[7] == 'C' and\
                    float(line_table[6]) == credit
            if debit:
                ok = ok and line_table[7] == 'D' and\
                    float(line_table[6]) == debit
            if ok:
                matches.append(data_line)
        self.assertEqual(
            len(matches), 1,
            "The line with journal %s ; account %s ; debit %d ; credit %d has"
            " not been found" % (journal_code, account_code, debit, credit))
