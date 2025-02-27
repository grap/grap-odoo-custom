# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestFoodMenuTag(TransactionCase):
    def setUp(self):
        super().setUp()
        self.tag_parent = self.env.ref("mrp_food_menu_tag.demo_tag_ecological")
        self.tag_vegan = self.env.ref("mrp_food_menu_tag.demo_tag_vegan")
        self.tag_halal = self.env.ref("mrp_food_menu_tag.demo_tag_halal")
        self.menu_revolution = self.env.ref(
            "mrp_food_menu_tag.demo_menu_french_revolution"
        )

    def test_01_bom_qty(self):
        self.assertEqual(
            self.tag_halal.food_menu_qty,
            0,
        )
        self.menu_revolution.write(
            {
                "food_menu_tag_ids": [
                    (6, 0, [self.tag_halal.id]),
                ]
            }
        )
        self.assertEqual(
            self.tag_halal.food_menu_qty,
            1,
        )

    def test_02_name_get(self):
        name_get_simple = self.tag_vegan.name_get()
        name_get_complete = self.tag_vegan.with_context(
            display_complete_name=True
        ).name_get()
        self.assertEqual(name_get_simple[0][1], "Vegan")
        self.assertEqual(name_get_complete[0][1], "Ecological / Vegan")
