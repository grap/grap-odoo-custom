# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestSeasonality(TransactionCase):
    def setUp(self):
        super(TestSeasonality, self).setUp()
        self.main_category = self.env.ref("product.product_category_all")
        self.seasonality_spring = self.env.ref("mrp_food.demo_seasonality_spring")

    def test_01_seasonality_add_period(self):
        spring_periods_qty = len(self.seasonality_spring.seasonality_line_ids)
        self.seasonality_spring.add_seasonality_line_one_more_year()
        self.assertEqual(
            len(self.seasonality_spring.seasonality_line_ids),
            spring_periods_qty + 1,
        )
        self.assertEqual(
            self.seasonality_spring.seasonality_line_ids[1].name, "Spring (2023)"
        )

    def test_02_seasonality_check_default_product(self):
        self.seasonality_spring.use_by_default_product = True
        product = self.env["product.product"].create(
            {
                "name": "Product",
                "categ_id": self.main_category.id,
            }
        )
        self.assertEqual(len(product.product_seasonality_ids), 1)
        self.assertEqual(
            product.product_seasonality_ids[0].id, self.seasonality_spring.id
        )

    def test_03_seasonality_check_default_bom(self):
        # First test
        # Create product and bom
        product2 = self.env["product.product"].create(
            {
                "name": "Test product",
                "categ_id": self.main_category.id,
            }
        )
        bom = self.env["mrp.bom"].create(
            {
                "product_id": product2.id,
                "product_tmpl_id": product2.product_tmpl_id.id,
            }
        )
        self.assertEqual(len(bom.bom_season_ids), 0)
        # Set season
        self.seasonality_spring.use_by_default_bom = True
        # Second test
        bom2 = self.env["mrp.bom"].create(
            {
                "product_id": product2.id,
                "product_tmpl_id": product2.product_tmpl_id.id,
            }
        )
        self.assertEqual(len(bom2.bom_season_ids), 1)
        self.assertEqual(bom2.bom_season_ids[0].id, self.seasonality_spring.id)
