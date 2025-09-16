# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestModule(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.po1 = cls.env.ref("purchase.purchase_order_1")
        cls.report_model = cls.env["ir.actions.report"]

    def test_01_purchase_order_report(self):
        self.report_model._render(
            "fermente_report_purchase.purchase_order_xlsx", self.po1.ids, False
        )
        self.report_model._render(
            "purchase.action_report_purchase_order", self.po1.ids, False
        )
        self.report_model._render(
            "purchase.report_purchase_quotation", self.po1.ids, False
        )
