# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestFoodMenu(TransactionCase):
    def setUp(self):
        super().setUp()
        # Objects
        self.food_menu_obj = self.env["mrp.food.menu"]
        self.food_menu_line_obj = self.env["mrp.food.menu.line"]
        self.product_product_obj = self.env["product.product"]
        self.mrp_bom_obj = self.env["mrp.bom"]
        # Datas
        self.uom_kg = self.env.ref("uom.product_uom_kgm")
        self.uom_unit = self.env.ref("uom.product_uom_unit")
        # Demo datas
        self.menu_revolution = self.env.ref("mrp_food_menu.demo_menu_french_revolution")
        # Creating Products
        self.product_seitan_bourguignon = self.product_product_obj.create(
            {
                "name": "Seitan bourguignon",
                "type": "product",
                "uom_id": self.uom_kg.id,
                "uom_po_id": self.uom_kg.id,
            }
        )

    def test_01_get_menu_info(self):
        self.assertEqual(self.menu_revolution.product_wo_bom_qty, 2)

        self.food_menu_line_obj.create(
            {
                "menu_id": self.menu_revolution.id,
                "product_id": self.product_seitan_bourguignon.id,
                "product_uom_qty": 3,
            }
        )
        self.assertEqual(self.menu_revolution.product_wo_bom_qty, 3)
