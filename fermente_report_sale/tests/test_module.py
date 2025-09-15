# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# from odoo.tests import tagged
from odoo.tests.common import TransactionCase


# @tagged("post_install", "-at_install")
class TestModule(TransactionCase):
    # def _render_html(self, xml_id_action, xml_id_item):
    #     action = self.env.ref(xml_id_action)
    #     item = self.env.ref(xml_id_item)
    #     action.render_qweb_html(item.ids)

    def _render(self, xml_id_action, xml_id_item):
        action = self.env.ref(xml_id_action)
        item = self.env.ref(xml_id_item)
        action.render(item.ids)

    def test_01_sale_order_report(self):
        self._render("sale.action_report_saleorder", "sale.sale_order_1")
