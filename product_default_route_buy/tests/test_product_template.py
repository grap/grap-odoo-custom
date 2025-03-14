# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductTemplate(TransactionCase):
    def setUp(self):
        super().setUp()
        self.BuyRoute = self.env.ref("purchase_stock.route_warehouse0_buy")
        self.ProductTemplate = self.env["product.template"]

        self.product_tmpl = self.ProductTemplate.create(
            {"name": "Test Product", "purchase_ok": False, "route_ids": []}
        )

    def test_01_onchange_adds_route(self):
        """Enabling purchase_ok adds Buy route"""
        self.assertNotIn(self.BuyRoute, self.product_tmpl.route_ids)

        self.product_tmpl.purchase_ok = True
        self.product_tmpl._onchange_purchase_ok()

        self.assertIn(self.BuyRoute, self.product_tmpl.route_ids)

    def test_02_onchange_removes_route(self):
        """Disabling purchase_ok removes Buy route"""
        self.product_tmpl.purchase_ok = True
        self.product_tmpl._onchange_purchase_ok()

        self.assertIn(self.BuyRoute, self.product_tmpl.route_ids)

        self.product_tmpl.purchase_ok = False
        self.product_tmpl._onchange_purchase_ok()

        self.assertNotIn(self.BuyRoute, self.product_tmpl.route_ids)
