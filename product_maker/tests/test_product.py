# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductTemplateMaker(TransactionCase):
    def setUp(self):
        super().setUp()
        self.product_template = self.env["product.template"].create(
            {
                "name": "Test Product",
            }
        )
        self.product_variant = self.product_template.product_variant_id

    def test_maker_description(self):
        self.product_template.maker_description = "Anticapitalist maker"
        self.assertEqual(self.product_variant.maker_description, "Anticapitalist maker")

        # Change the variant field
        self.product_variant.maker_description = "Capitalist Maker"
        self.product_template._compute_template_field_from_variant_field(
            "maker_description"
        )
        self.assertEqual(self.product_template.maker_description, "Capitalist Maker")
