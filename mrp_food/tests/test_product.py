# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests.common import TransactionCase


class TestProductProduct(TransactionCase):
    def setUp(self):
        super(TestProductProduct, self).setUp()
        self.product_product_desk = self.env.ref("product.product_product_3")
        self.bom_desk = self.env.ref("mrp.mrp_bom_manufacture")

    def test_01_onchange_date_last_statement_price(self):
        self.product_product_desk.write({"standard_price": 10})
        self.product_product_desk._onchange_date_last_statement_price()
        self.assertEqual(
            self.product_product_desk.date_last_statement_price,
            fields.Date.today(),
        )
