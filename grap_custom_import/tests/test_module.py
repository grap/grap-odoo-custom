# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.modules.module import get_module_resource
from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    def _test_import_file(self, file_name, model):

        csv_file_path = get_module_resource("grap_custom_import", "tests", file_name)
        file_content = open(csv_file_path, "rb").read()
        import_wizard = self.env["base_import.import"].create(
            {
                "res_model": model,
                "file": file_content,
                "file_type": "text/csv",
            }
        )

        result = import_wizard.parse_preview(
            {
                "headers": True,
                "quoting": '"',
            }
        )
        self.assertIsNone(result.get("error"))

    def test_import_product(self):
        self._test_import_file("template_import_product.csv", "product.product")

    def test_import_supplier(self):
        self._test_import_file("template_import_supplier.csv", "res.partner")
