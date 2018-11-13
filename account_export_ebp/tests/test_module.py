# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.WizardEbpExport = self.env['wizard.ebp.export']
        self.move_1 = self.env.ref('account.invoice_1').move_id

    # Test Section
    def test_01_export_move(self):
        wizard = self.WizardEbpExport.with_context(
            active_ids=[self.move_1.id]).create({})

        wizard.button_export()

        self.assertNotEqual(
            wizard.ebp_export_id.id, False,
            "Export a move should create an ebp export")

        self.assertEqual(
            wizard.ebp_export_id, self.move_1.ebp_export_id,
            "Exporting a move should link it to the ebp export created.")
