# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestStandardPrice(TransactionCase):
    def setUp(self):
        super(TestStandardPrice, self).setUp()
        # Product and its supplier info
        self.office_chair = self.env.ref("product.product_delivery_01")
        self.office_chair_std_p = self.office_chair.standard_price
        self.office_chair_suppinfo = self.office_chair.variant_seller_ids[0]
        self.office_chair_suppinfo_price = self.office_chair_suppinfo.price
        # Others
        self.uom_dozen = self.env.ref("uom.product_uom_dozen")

    def test_01_set_new_price(self):
        # Changing Standard price with supplier info
        self.office_chair_suppinfo.set_product_standard_price_from_supplierinfo()
        self.assertEqual(
            self.office_chair_suppinfo_price,
            self.office_chair.standard_price,
        )

    # Test if product standard price is well calculated with purchase uom
    def test_02_change_po_uom(self):
        self.office_chair.uom_po_id = self.uom_dozen
        self.office_chair_suppinfo.set_product_standard_price_from_supplierinfo()
        self.assertEqual(
            self.office_chair_suppinfo_price / self.uom_dozen.factor_inv,
            self.office_chair.standard_price,
        )
