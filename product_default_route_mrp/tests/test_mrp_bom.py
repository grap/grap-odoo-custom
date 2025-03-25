# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.tests.common import TransactionCase


class TestMrpBom(TransactionCase):
    def setUp(self):
        super().setUp()
        self.ManufactureRoute = self.env.ref("mrp.route_warehouse0_manufacture")
        self.ProductTemplate = self.env["product.template"]
        self.MrpBom = self.env["mrp.bom"]

        # Create a test product
        self.product_tmpl = self.ProductTemplate.create({"name": "Test Product"})

    def test_01_create_bom_adds_route(self):
        """Creating a BoM should assign the manufacture route to its product"""
        self.assertNotIn(self.ManufactureRoute, self.product_tmpl.route_ids)

        bom = self.MrpBom.create(
            {"product_tmpl_id": self.product_tmpl.id, "type": "normal"}
        )

        self.assertIn(self.ManufactureRoute, self.product_tmpl.route_ids)

        bom.unlink()

    def test_02_unlink_bom_removes_route(self):
        """Deleting the last BoM should remove the manufacture route from its product"""
        bom = self.MrpBom.create(
            {"product_tmpl_id": self.product_tmpl.id, "type": "normal"}
        )

        self.assertIn(self.ManufactureRoute, self.product_tmpl.route_ids)

        bom.unlink()

        self.assertNotIn(self.ManufactureRoute, self.product_tmpl.route_ids)
