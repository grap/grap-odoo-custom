# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMrpBomLineWeight(TransactionCase):
    def setUp(self):
        super(TestMrpBomLineWeight, self).setUp()
        self.bom_tomato_pie = self.env.ref("mrp_business.demo_bom_tomato_pie")
        self.bom_tomato_pie_tomatoes = self.env.ref(
            "mrp_business.demo_bom_tomato_pie_line_tomatoes"
        )
        self.bom_tomato_pie_spinach = self.env.ref(
            "mrp_business.demo_bom_tomato_pie_line_spinach"
        )
        self.bom_tomato_pie_mustard = self.env.ref(
            "mrp_business.demo_bom_tomato_pie_line_mustard"
        )
        self.bom_tomato_pie_pie = self.env.ref(
            "mrp_business.demo_bom_tomato_pie_line_pie"
        )

    def test_01_set_products_weight_check_bom(self):
        # Values from demo datas
        total_weight_theorical = 0.5 + 0.3 + 0.1 + 0.2
        self.assertEqual(
            self.bom_tomato_pie.bom_components_total_weight, total_weight_theorical
        )

    def test_02_change_bom_line_qty(self):
        # Double mustard
        self.bom_tomato_pie_mustard.product_qty = 0.2
        total_weight_theorical = 0.5 + 0.3 + 0.2 + 0.2
        self.assertEqual(
            self.bom_tomato_pie.bom_components_total_weight, total_weight_theorical
        )
