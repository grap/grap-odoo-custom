# coding: utf-8
# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.Wizard = self.env['wizard.multi.charts.accounts']
        self.ResCompany = self.env['res.company']
        self.french_chart_of_account = self.env.ref(
            'l10n_fr.l10n_fr_pcg_chart_template')
        self.euro = self.env.ref('base.EUR')

    # Test Section
    def test_01_create_new_chart_of_account(self):

        # Create a new company
        company = self.ResCompany.create({
            'name': 'Test Company (GRAP - L10n_fr',
            'currency_id': self.euro.id,
        })
        wizard = self.Wizard.create({
            'company_id': company.id,
            'chart_template_id': self.french_chart_of_account.id,
            'code_digits': 3,
            'complete_tax_set': self.french_chart_of_account.complete_tax_set,
            'currency_id': company.currency_id.id,
        })
        wizard.execute()
