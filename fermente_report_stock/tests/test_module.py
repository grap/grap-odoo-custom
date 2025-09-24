# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestModule(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stock1 = cls.env.ref("stock.outgoing_shipment_main_warehouse")
        cls.report_model = cls.env["ir.actions.report"]

    def test_01_stock_picking_report(self):
        self.report_model._render("stock.action_report_picking", self.stock1.ids, False)
        self.report_model._render(
            "stock.action_report_delivery", self.stock1.ids, False
        )
