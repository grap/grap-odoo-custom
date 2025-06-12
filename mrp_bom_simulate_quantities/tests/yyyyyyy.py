# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPPPPP(TransactionCase):
    def setUp(self):
        super().setUp()

        self.uom_kg = self.env.ref("uom.product_uom_kgm")
        self.uom_unit = self.env.ref("uom.product_uom_unit")
        self.product_model = self.env["product.product"]
        self.bom_model = self.env["mrp.bom"]
        self.bom_line_model = self.env["mrp.bom.line"]

        # Creating Products
        self.product_cookie = self.product_model.create(
            {
                "name": "Cookie",
                "type": "product",
                "uom_id": self.uom_kg.id,
                "uom_po_id": self.uom_kg.id,
            }
        )

    def test_01_ggggggg(self):
        """Explain test"""
        self.assertEqual(, )
