# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestFoodMenu(TransactionCase):
    def setUp(self):
        super().setUp()
        # Objects
        self.food_menu_line_obj = self.env["mrp.food.menu.line"]
        self.mrp_bom_obj = self.env["mrp.bom"]
        # Demo datas
        self.menu_revolution = self.env.ref("mrp_food_menu.demo_menu_french_revolution")
        self.product_arachide = self.env.ref("product_food.product_arachide_toaste")
        self.product_arachide_template = self.env.ref(
            "product_food.product_arachide_toaste_product_template"
        )
        # Create BoM
        self.bom_arachide = self.mrp_bom_obj.create(
            {
                "product_tmpl_id": self.product_arachide_template.id,
            }
        )

    def test_01_get_menu_allergens(self):
        self.menu_revolution._compute_menu_allergen_ids()
        self.assertEqual(len(self.menu_revolution.menu_allergen_ids), 2)
        self.assertEqual(self.menu_revolution.menu_allergen_ids[0].code, "SES")

        self.food_menu_line_obj.create(
            {
                "menu_id": self.menu_revolution.id,
                "product_id": self.product_arachide.id,
                "bom_id": self.bom_arachide.id,
            }
        )
        self.menu_revolution._compute_menu_allergen_ids()
        self.assertEqual(len(self.menu_revolution.menu_allergen_ids), 3)
