# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestSeller(TransactionCase):
    def setUp(self):
        super(TestSeller, self).setUp()
        self.product_workplace = self.env.ref("product.product_product_24")
        self.product_acoustic = self.env.ref("product.product_product_25")
        self.product_with_var_chair = self.env.ref("product.product_product_11")
        self.product_without_seller_desk = self.env.ref("product.product_product_3")

        self.partner_woodcorner = self.env.ref("base.res_partner_1")
        self.partner_azure = self.env.ref("base.res_partner_12")

    def test_01_computed_main_vendor(self):
        self.assertEqual(
            self.product_acoustic.product_main_seller_partner_id,
            self.product_acoustic.seller_ids[0].name,
        )
        self.assertEqual(
            self.product_with_var_chair.product_main_seller_partner_id,
            self.product_acoustic.product_variant_ids[0].variant_seller_ids[0].name,
        )

    def test_02_replace_vendor(self):
        self.product_acoustic.write({"seller_ids": [(5, 0)]})
        self.product_acoustic.write(
            {
                "seller_ids": [
                    (0, 0, {"name": self.partner_azure.id}),
                ]
            }
        )
        self.assertEqual(
            self.product_acoustic.product_main_seller_partner_id.id,
            self.partner_azure.id,
        )

    def test_03_add_vendor(self):
        # Add one supplierinfo at the end
        # -- For product without vendor
        self.product_without_seller_desk.write(
            {
                "seller_ids": [
                    (0, 0, {"name": self.partner_azure.id}),
                ]
            }
        )
        self.assertEqual(
            self.product_without_seller_desk.product_main_seller_partner_id.id,
            self.partner_azure.id,
        )
        # -- For product who had vendor
        self.product_workplace.write(
            {
                "seller_ids": [
                    (0, 0, {"sequence": 100, "name": self.partner_azure.id}),
                ]
            }
        )
        self.assertNotEqual(
            self.product_workplace.product_main_seller_partner_id.id,
            self.partner_azure.id,
        )
