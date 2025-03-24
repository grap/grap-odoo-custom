# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductReplenish(TransactionCase):
    def setUp(self):
        super().setUp()

        # Datas
        self.manufacture_route = self.env.ref("mrp.route_warehouse0_manufacture")
        self.warehouse_1 = self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.user.id)], limit=1
        )
        self.uom_unit = self.env.ref("uom.product_uom_unit")

        # Create datas
        self.product_test = self.env["product.product"].create(
            {"name": "Product Test", "route_ids": [(6, 0, [self.manufacture_route.id])]}
        )

    def test_01_product_replenish_launch_manufacture(self):
        replenish_wizard = self.env["product.replenish"].create(
            {
                "product_id": self.product_test.id,
                "product_tmpl_id": self.product_test.product_tmpl_id.id,
                "product_uom_id": self.uom_unit.id,
                "quantity": 42,
                "warehouse_id": self.warehouse_1.id,
            }
        )

        replenish_wizard.launch_replenishment()
        # import pdb; pdb.set_trace()
        last_mo = self.env["mrp.production"].search(
            [("origin", "=", "Manual Replenishment")]
        )[-1]
        self.assertTrue(last_mo.origin, "Picking not found")
        self.assertEqual(
            last_mo.product_id, self.product_test, "Wrong Product on MO created"
        )
        self.assertEqual(last_mo.product_qty, 42, "Quantities does not match")
