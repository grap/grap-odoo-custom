# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# from odoo.tests import tagged
from odoo.tests.common import TransactionCase


# @tagged("post_install", "-at_install")
class TestModule(TransactionCase):

    def _render_html(self, xml_id_action, xml_id_item):
        action = self.env.ref(xml_id_action)
        item = self.env.ref(xml_id_item)
        action.render_qweb_html(item.ids)

    def test_01_sale_order_report(self):
        self._render_html("sale.action_report_saleorder", "sale.sale_order_1")

    def test_02_purchase_order_report(self):
        self._render_html(
            "purchase.action_report_purchase_order",
            "purchase.purchase_order_1"
        )
        self._render_html(
            "purchase.report_purchase_quotation",
            "purchase.purchase_order_1"
        )

    def test_03_stock_picking_report(self):
        self._render_html(
            "stock.action_report_picking",
            "stock.outgoing_shipment_main_warehouse"
        )
        self._render_html(
            "stock.action_report_delivery",
            "stock.outgoing_shipment_main_warehouse"
        )

    def test_04_stock_inventory_report(self):
        self._render_html(
            "stock.action_report_inventory",
            "stock.stock_inventory_0"
        )

    def _test_05_account_invoice_report(self):
        # TODO, make demo data. There are no demo invoices
        pass

    def test_06_product_product_report(self):
        # Barcode report (without barcode)
        self._render_html(
            "grap_qweb_report.report_product_product_barcode_5",
            "product_food.product_arachide_toaste"
        )
        # Barcode report (with barcode)
        self._render_html(
            "grap_qweb_report.report_product_product_barcode_5",
            "point_of_sale.desk_organizer"
        )
