# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestModule(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Copy paste code (AGPL-3.0) from OCA module
        # sale_order_invoicing_grouping_criteria
        # Copyright 2019 Tecnativa - Pedro M. Baeza
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        if not cls.env.company.chart_template_id:
            # Load a CoA if there's none in current company
            coa = cls.env.ref("l10n_generic_coa.configurable_chart_template", False)
            if not coa:
                # Load the first available CoA
                coa = cls.env["account.chart.template"].search(
                    [("visible", "=", True)], limit=1
                )
            coa.try_loading(company=cls.env.company, install_demo=False)
        # End

        cls.sale1 = cls.env.ref("sale.sale_order_1")
        cls.sale6 = cls.env.ref("sale.sale_order_6")
        cls.report_model = cls.env["ir.actions.report"]
        cls.product_categ = cls.env["product.category"].create(
            {"name": "Test category"}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Gilet jaune",
                "categ_id": cls.product_categ.id,
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "list_price": 1000.00,
                "standard_price": 500.00,
                "type": "product",
                "invoice_policy": "order",
            }
        )
        cls.order1 = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        False,
                        {
                            "product_id": cls.product.id,
                            "product_uom_qty": 117,
                            "product_uom": cls.product.uom_id.id,
                            "price_unit": 1000.00,
                        },
                    ),
                ],
            }
        )
        cls.order1.action_confirm()
        cls.order2 = cls.order1.copy()
        cls.order2.action_confirm()

    def test_01_sale_order_report(self):
        self.report_model._render("sale.action_report_saleorder", self.sale1.ids, False)

    def test_02_sale_order_add_prefix(self):
        # Weirdly, grouped needs to be False to have one invoice
        invoice_id = (self.order1 + self.order2)._create_invoices(grouped=False)
        picking_date_str = self.order1.picking_ids[0].date.strftime("%Y-%m-%d") + " - "
        self.assertEqual(invoice_id.line_ids[0].name, picking_date_str + "Gilet jaune")
