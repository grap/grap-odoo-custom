# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestFoodMenu(TransactionCase):
    def setUp(self):
        super().setUp()
        self.food_menu = self.env.ref("mrp_food_menu.demo_menu_french_revolution")
        self.houmous = self.env.ref("mrp_food_menu.demo_houmous")
        self.quiche = self.env.ref("mrp_food_menu.demo_quiche")
        self.partner = self.env.ref("base.res_partner_1")

    def test_01_compute_sale_order_count(self):
        self.food_menu.sale_order_ids = [(0, 0, {"partner_id": self.partner.id})]
        self.food_menu._compute_sale_order_count()
        self.assertEqual(self.food_menu.sale_order_count, 1)

    def test_02_create_sale_order_from_menu(self):
        action = self.food_menu.create_sale_order_from_menu()

        # Verify the sale order lines contain the correct products
        order_lines = action["context"]["default_order_line"]
        product_ids = []
        for line in order_lines:
            product_ids.append(line[2]["product_id"])

        self.assertIn(self.houmous.id, product_ids)
        self.assertIn(self.quiche.id, product_ids)
