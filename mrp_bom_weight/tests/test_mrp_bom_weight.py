# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMrpBomWeight(TransactionCase):
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

        self.margarine = self.product_model.create(
            {
                "name": "Margarine",
                "type": "product",
                "uom_id": self.uom_kg.id,
                "uom_po_id": self.uom_kg.id,
            }
        )

        self.chocolate = self.product_model.create(
            {
                "name": "Chocolate",
                "type": "product",
                "uom_id": self.uom_kg.id,
                "uom_po_id": self.uom_kg.id,
            }
        )

        self.small_packet = self.product_model.create(
            {
                "name": "Small packet",
                "type": "product",
                "uom_id": self.uom_unit.id,
                "uom_po_id": self.uom_unit.id,
                "net_weight": 0.1,
            }
        )

        # Creating BoM
        self.bom_cookie = self.bom_model.create(
            {
                "product_tmpl_id": self.product_cookie.product_tmpl_id.id,
                "product_uom_id": self.uom_kg.id,
                "type": "normal",
                "product_qty": 1.6,
            }
        )

        self.bom_cookie_line_1 = self.bom_line_model.create(
            {
                "bom_id": self.bom_cookie.id,
                "product_id": self.margarine.id,
                "product_qty": 1,
                "product_qty_net": 1,
                "product_uom_id": self.uom_kg.id,
            }
        )

        self.bom_cookie_line_2 = self.bom_line_model.create(
            {
                "bom_id": self.bom_cookie.id,
                "product_id": self.chocolate.id,
                "product_qty": 0.5,
                "product_qty_net": 0.5,
                "product_uom_id": self.uom_kg.id,
            }
        )

        self.bom_cookie_line_3 = self.bom_line_model.create(
            {
                "bom_id": self.bom_cookie.id,
                "product_id": self.small_packet.id,
                "product_qty": 1.0,
                "product_qty_net": 1.0,
                "product_uom_id": self.uom_unit.id,
            }
        )

        # Compute all values
        self.bom_cookie_line_1._compute_line_gross_weight()
        self.bom_cookie_line_2._compute_line_gross_weight()
        self.bom_cookie_line_3._compute_line_gross_weight()

        self.bom_cookie_line_1._compute_line_net_weight()
        self.bom_cookie_line_2._compute_line_net_weight()
        self.bom_cookie_line_3._compute_line_net_weight()

        # Computing one line percentage triggers other lines
        self.bom_cookie_line_1._compute_line_net_weight_percentage()

        self.bom_cookie._compute_bom_components_total_net_weight()
        self.bom_cookie._compute_bom_components_total_gross_weight()

    def test_01_bom_weights(self):
        # Weightable product 1 + 0,5 + Unit product with its weight 0,1
        self.assertEqual(self.bom_cookie.bom_components_total_net_weight, 1.6)

    def test_02_bom_net_weight_percentage(self):
        # Weightable product 1 + 0,5 + Unit product with its weight 0,1
        self.assertEqual(self.bom_cookie_line_1.line_net_weight_percentage, 62.5)
        self.assertEqual(self.bom_cookie_line_2.line_net_weight_percentage, 31.25)
        self.assertEqual(self.bom_cookie_line_3.line_net_weight_percentage, 6.25)

        # Changing one value to test computing of all percentages
        self.bom_cookie_line_1.product_qty_net = 0.5
        self.bom_cookie_line_1._compute_line_net_weight_percentage()
        self.assertEqual(
            round(self.bom_cookie_line_1.line_net_weight_percentage, 2), 45.45
        )
        self.assertEqual(
            round(self.bom_cookie_line_2.line_net_weight_percentage, 2), 45.45
        )
        self.assertEqual(
            round(self.bom_cookie_line_3.line_net_weight_percentage, 2), 9.09
        )

    def test_03_bom_display_set_quantity_with_net_quantities(self):
        # At first, BoM product_qty is correct
        self.bom_cookie._compute_display_set_quantity_with_net_quantities()
        self.assertEqual(
            self.bom_cookie.display_set_quantity_with_net_quantities, False
        )

        # Change one value
        self.bom_cookie_line_1.product_qty_net = 2
        self.bom_cookie._compute_display_set_quantity_with_net_quantities()
        self.assertEqual(self.bom_cookie.display_set_quantity_with_net_quantities, True)

        # Use button to adjust quantity
        self.bom_cookie.set_bom_quantity_with_net_quantities()
        self.assertEqual(
            self.bom_cookie.display_set_quantity_with_net_quantities, False
        )
