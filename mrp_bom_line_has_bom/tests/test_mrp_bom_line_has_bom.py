# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMrpBomLineHasBom(TransactionCase):
    def setUp(self):
        super(TestMrpBomLineHasBom, self).setUp()
        self.bom_bourguignon = self.env.ref(
            "mrp_bom_line_has_bom.demo_bom_french_vegan_bourguignon"
        )
        self.bom_bourguignon_line_seitan = self.env.ref(
            "mrp_bom_line_has_bom.demo_bom_french_vegan_bourguignon_line_seitan"
        )
        self.bom_bourguignon_line_carrot = self.env.ref(
            "mrp_bom_line_has_bom.demo_bom_french_vegan_bourguignon_line_carrot"
        )
        self.product_seitan = self.env.ref("mrp_bom_line_has_bom.demo_product_seitan")
        self.product_carrot = self.env.ref("mrp_bom_line_has_bom.demo_product_carrot")

    def test_01_compute_has_bom(self):
        self.env["mrp.bom"].create(
            {
                "product_id": self.product_seitan.id,
                "product_tmpl_id": self.product_seitan.product_tmpl_id.id,
            }
        )
        self.product_seitan._compute_bom_count()
        self.assertEqual(self.bom_bourguignon_line_seitan.has_bom, True)
        self.assertEqual(self.bom_bourguignon_line_carrot.has_bom, False)

    def test_02_go_to_bom_form(self):
        # Just one BoM → we should go on Form View
        self.product_seitan._compute_bom_count()
        result = self.bom_bourguignon_line_seitan.go_to_bom()
        self.assertEqual(result["res_model"], "mrp.bom")
        self.assertEqual(result["type"], "ir.actions.act_window")
        self.assertTrue(result["views"][0][0], self.env.ref("mrp.mrp_bom_form_view").id)
        self.assertEqual(result["domain"], "[]")

    def test_03_go_to_bom_tree(self):
        # Create second BoM → we should go on Tree View
        self.env["mrp.bom"].create(
            {
                "product_id": self.product_seitan.id,
                "product_tmpl_id": self.product_seitan.product_tmpl_id.id,
            }
        )
        self.product_seitan._compute_bom_count()
        result2 = self.bom_bourguignon_line_seitan.go_to_bom()
        self.assertEqual(result2["res_model"], "mrp.bom")
        self.assertEqual(result2["type"], "ir.actions.act_window")
        self.assertEqual(
            result2["domain"], [("id", "in", self.product_seitan.bom_ids.ids)]
        )
