# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestSeasonality(TransactionCase):
    def setUp(self):
        super(TestSeasonality, self).setUp()
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
