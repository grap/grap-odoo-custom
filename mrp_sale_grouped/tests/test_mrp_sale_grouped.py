# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMrpSaleGrouped(TransactionCase):
    def setUp(self):
        super(TestMrpSaleGrouped, self).setUp()
        # Objects
        mrp_sale_grouped_obj = self.env["mrp.sale.grouped"]
        # Demo datas
        self.sale_order_gemini = self.env.ref("mrp_sale_grouped.demo_sale_gemini")
        self.sale_order_ready_mat = self.env.ref("mrp_sale_grouped.demo_sale_ready_mat")
        # Create one sale_grouped with sales
        self.mrp_sale_grouped_1 = mrp_sale_grouped_obj.create(
            {"name": "TEST Grouped Sale"}
        )
        # Add grouped to sales
        self.sale_order_gemini.mrp_sale_grouped_id = self.mrp_sale_grouped_1
        self.sale_order_ready_mat.mrp_sale_grouped_id = self.mrp_sale_grouped_1

    def test_01_create_grouped_check_sale_linked(self):
        self.assertEqual(self.mrp_sale_grouped_1.orders_qty, 2)

    def test_02_grouped_sales_check_confirm_quotations(self):
        self.assertEqual(self.mrp_sale_grouped_1.order_ids[0].state, "draft")
        self.assertEqual(self.mrp_sale_grouped_1.order_ids[1].state, "draft")
        self.mrp_sale_grouped_1.confirm_all_sale_order()
        self.assertEqual(self.mrp_sale_grouped_1.order_ids[0].state, "sale")
        self.assertEqual(self.mrp_sale_grouped_1.order_ids[1].state, "sale")
