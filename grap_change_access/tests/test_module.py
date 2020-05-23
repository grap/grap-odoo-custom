# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class TestModule(TransactionCase):
    def setUp(self):
        super(TestModule, self).setUp()
        self.demo_user = self.env.ref("base.user_demo")
        self.laptop_E5023 = self.env.ref(
            "product.product_product_25_product_template"
        )

    # Test Section
    def test_01_check_restricted_access_pos_product(self):
        with self.assertRaises(ValidationError):
            self.laptop_E5023.sudo(self.demo_user.id).write(
                {"expense_pdt": True}
            )

    def test_02_pos_use_sale_purchase_use(self):
        with self.assertRaises(ValidationError):
            self.laptop_E5023.write(
                {"sale_ok": True, "expense_pdt": True,}
            )

    def test_02_pos_use_bad_account(self):
        with self.assertRaises(ValidationError):
            self.laptop_E5023.write(
                {
                    "sale_ok": False,
                    "purchase_ok": False,
                    "expense_pdt": True,
                    "income_pdt": True,
                }
            )
