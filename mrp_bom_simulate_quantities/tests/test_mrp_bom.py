# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestMrpBomSimulation(TransactionCase):
    def setUp(self):
        super().setUp()
        self.bom = self.env.ref("mrp_bom_simulate_quantities.demo_bom_farmhouse_bread")
        self.product_flour = self.env.ref(
            "mrp_bom_simulate_quantities.demo_product_flour"
        )
        self.product_salt = self.env.ref(
            "mrp_bom_simulate_quantities.demo_product_salt"
        )
        self.product_levain = self.env.ref(
            "mrp_bom_simulate_quantities.demo_product_rye_levain"
        )
        self.product_water = self.env.ref(
            "mrp_bom_simulate_quantities.demo_product_water"
        )

    def test_01_single_product_simulation(self):
        self.bom.bom_simulate_product = self.product_flour
        self.bom.bom_simulate_product_qty = 2.0
        self.bom._compute_bom_simulate_bom_lines_and_qty()

        flour_line = self.bom.bom_simulate_bom_lines.filtered(
            lambda x: x.product_id == self.product_flour
        )
        self.assertEqual(flour_line.product_qty, 2.0)

        expected_ratio = 2.0 / 1.0
        water_line = self.bom.bom_simulate_bom_lines.filtered(
            lambda x: x.product_id == self.product_water
        )
        self.assertEqual(water_line.product_qty, 0.72 * expected_ratio)

    def test_02_product_simulation_product_1_limits(self):
        self.bom.write(
            {
                "show_second_product": True,
                "bom_simulate_product": self.product_flour,
                "bom_simulate_product_qty": 2.0,
                "bom_simulate_product_2": self.product_water,
                "bom_simulate_product_qty_2": 1.45,
            }
        )
        self.bom._compute_bom_simulate_bom_lines_and_qty()
        self.assertEqual(self.bom.limiting_product, self.product_flour)

    def test_03_product_simulation_product_2_limits(self):
        self.bom.write(
            {
                "show_second_product": True,
                "bom_simulate_product": self.product_flour,
                "bom_simulate_product_qty": 2.0,
                "bom_simulate_product_2": self.product_water,
                "bom_simulate_product_qty_2": 1.43,
            }
        )
        self.bom._compute_bom_simulate_bom_lines_and_qty()
        self.assertEqual(self.bom.limiting_product, self.product_water)

    def test_04_csv_export_simulation(self):
        self.bom.bom_simulate_product = self.product_flour
        self.bom.bom_simulate_product_qty = 2.0
        self.bom._compute_bom_simulate_bom_lines_and_qty()

        action = self.bom.action_export_simulation_csv()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertIn("/web/content/", action["url"])
