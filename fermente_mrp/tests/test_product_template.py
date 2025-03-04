# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductTemplate(TransactionCase):
    def setUp(self):
        super().setUp()
        self.manufacture_route = self.env.ref("mrp.route_warehouse0_manufacture")

        self.product_test = self.env["product.template"].create(
            {
                "name": "Product Test",
            }
        )

        self.bom = self.env["mrp.bom"].create(
            {
                "product_tmpl_id": self.product_test.id,
                "product_qty": 1.0,
            }
        )

    def test_01_compute_bom_count_with_bom(self):
        self.product_test._compute_bom_count()

        self.assertIn(
            self.manufacture_route,
            self.product_test.route_ids,
            "Manufacturing route should have been added.",
        )

    def test_02_compute_bom_count_without_bom(self):
        self.bom.unlink()
        self.product_test._compute_bom_count()

        self.assertNotIn(
            self.manufacture_route,
            self.product_test.route_ids,
            "Manufacturing route should have been deleted.",
        )
