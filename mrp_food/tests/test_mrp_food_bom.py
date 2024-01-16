# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestMrpFoodBom(TransactionCase):
    def setUp(self):
        super(TestMrpFoodBom, self).setUp()
        self.bom_tomato_tart = self.env.ref("mrp_food.demo_bom_tomato_tart")
        self.bom_not_seasonal = self.env.ref("mrp_food.demo_bom_lines_not_seasonal")
        self.bom_tomato_tart_tomatoes = self.env.ref(
            "mrp_food.demo_bom_tomato_tart_line_tomatoes"
        )
        self.seasonality_all = self.env.ref("mrp_food.demo_seasonality_all_season")
        self.peach = self.env.ref("mrp_food.demo_product_peach_no_season")

    def test_01_bom_price_subtotal_line(self):
        self.assertEqual(
            self.bom_tomato_tart_tomatoes.standard_price_subtotal,
            1.5,
        )
        self.bom_tomato_tart_tomatoes.product_qty = 1
        self.assertEqual(
            self.bom_tomato_tart_tomatoes.standard_price_subtotal,
            3,
        )

    def test_02_bom_price_total(self):
        self.assertEqual(
            self.bom_tomato_tart.standard_price_total,
            6.7,
        )
        self.bom_tomato_tart.write({"bom_line_ids": [(5, 0)]})
        self.assertEqual(
            self.bom_tomato_tart.standard_price_total,
            0,
        )

    def test_03_seasonality_check_constrains(self):
        new_seasonality_line = self.env["seasonality.line"].create(
            {"name": "Wrong line", "date_start": "2024-01-01", "date_end": "2025-01-01"}
        )
        with self.assertRaises(ValidationError):
            new_seasonality_line.write({"date_end": "2023-01-01"})

    def test_04_bom_seasonality(self):
        self.bom_tomato_tart.write({"bom_season_ids": [(5, 0)]})
        self.assertEqual(
            self.bom_tomato_tart.is_bom_seasonal,
            False,
        )
        self.bom_tomato_tart.write({"bom_season_ids": [(4, self.seasonality_all.id)]})
        self.assertEqual(
            self.bom_tomato_tart.is_bom_seasonal,
            True,
        )

    def test_05_bom_lines_seasonalities(self):
        self.assertEqual(self.bom_not_seasonal.products_not_in_season, "Chickpea.")
        self.bom_not_seasonal.write(
            {"bom_line_ids": [(0, 0, {"product_id": self.peach.id, "product_qty": 1})]}
        )
        self.assertEqual(
            self.bom_not_seasonal.products_not_in_season, "Chickpea, Peach."
        )
