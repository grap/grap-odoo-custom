# @author Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import tagged
from odoo.tests.common import Form, TransactionCase


@tagged("post_install", "-at_install")
class TestFermenteBaseProductMassAddition(TransactionCase):
    @classmethod
    def _add_seller(cls, product, sellers):
        product.seller_ids.filtered(lambda s: s.partner_id == cls.partner).unlink()

        for seller in sellers:
            cls.env["product.supplierinfo"].create(
                {
                    "product_tmpl_id": product.product_tmpl_id.id,
                    "partner_id": cls.partner.id,
                    "min_qty": seller.get("min_qty", 0),
                    "price": seller.get("price", 0),
                    "multiplier_qty": seller.get("multiplier_qty", 0),
                    "discount": seller.get("discount", 0),
                    "discount2": seller.get("discount2", 0),
                }
            )

    @classmethod
    def _setUpBasicPurchaseOrder(cls):
        vals = {"partner_id": cls.partner.id}
        if hasattr(cls.env["purchase.order"], "order_type"):
            vals["order_type"] = cls.env.ref("purchase_order_type.po_type_blanket").id
        cls.po = cls.env["purchase.order"].create(vals)
        with Form(cls.po, "purchase.purchase_order_form") as po_form:
            po_form.partner_id = cls.partner
        ctx = {"parent_id": cls.po.id, "parent_model": "purchase.order"}
        cls.product_1 = cls.product_1.with_context(**ctx)
        cls.product_2 = cls.product_2.with_context(**ctx)
        cls.product_3 = cls.product_3.with_context(**ctx)
        # cls.product_1.qty_to_process = 5.0
        # cls.product_2.qty_to_process = 6.0
        # cls.product_3.qty_to_process = 7.0

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.product_1 = cls.env.ref("product.product_product_8")
        cls.product_2 = cls.env.ref("product.product_product_11")
        cls.product_3 = cls.env.ref("product.product_product_6")

        cls._add_seller(
            cls.product_1,
            [
                {"min_qty": 0, "price": 1789},
                {"min_qty": 7, "price": 1871},
            ],
        )

        cls._add_seller(
            cls.product_2,
            [
                {"min_qty": 0, "price": 117, "multiplier_qty": 2},
                {"min_qty": 40, "price": 217, "multiplier_qty": 20},
            ],
        )

        cls._add_seller(
            cls.product_3,
            [
                {"min_qty": 10, "price": 20, "multiplier_qty": 10},
            ],
        )

        cls._setUpBasicPurchaseOrder()

    # With Product 01, get the right supplier price (the first ont )
    def test_01_supplier_price_selection(self):
        self.product_1.qty_to_process = 12  # whatever
        self.product_1._compute_mass_addition_purchase()
        self.assertEqual(self.product_1.mass_addition_purchase_price, 1789)

    # With Product 02, multiplier quantity 5 will be bad
    def test_02_multiplier_bad(self):
        self.product_2.qty_to_process = 5
        self.product_2._compute_mass_addition_purchase()
        self.product_2._compute_mass_addition_purchase_bad()
        self.assertTrue(self.product_2.mass_addition_purchase_multiplier_qty_bad)

    # With Product 02 multiplier quantity 6 will be bad
    def test_03_multiplier_ok(self):
        self.product_2.qty_to_process = 6
        self.product_2._compute_mass_addition_purchase()
        self.product_2._compute_mass_addition_purchase_bad()
        self.assertFalse(self.product_2.mass_addition_purchase_multiplier_qty_bad)

    # With Product 03, minimum quantity 2 will be bad
    def test_04_min_qty_bad(self):
        print("========== test_04_min_qty_bad")
        self.product_3.qty_to_process = 2
        import pdb

        pdb.set_trace()
        # self.product_3._compute_mass_addition_purchase()
        self.product_3._compute_mass_addition_purchase_bad()
        self.assertTrue(self.product_3.mass_addition_purchase_min_qty_bad)

    # With Product 03, minimum quantity 6 will be good
    def test_05_min_qty_ok(self):
        self.product_3.qty_to_process = 11
        self.product_3._compute_mass_addition_purchase()
        self.product_3._compute_mass_addition_purchase_bad()
        self.assertFalse(self.product_3.mass_addition_purchase_min_qty_bad)

    # With no supplier
    def test_06_no_supplier(self):
        product = self.env["product.product"].create(
            {
                "name": "Test Product",
            }
        )

        product = product.with_context(
            parent_id=self.po.id, parent_model="purchase.order"
        )

        product.qty_to_process = 5
        product._compute_mass_addition_purchase()

        self.assertEqual(product.mass_addition_purchase_price, 0)

    # def test_product_seller_price(self):
    #     self.assertEqual(self.product_1.seller_price, 10)
    #     self.product_1.qty_to_process = 10.0
    #     self.assertEqual(self.product_1.seller_price, 8)
    #     self.product_1.quick_uom_id = self.uom_dozen
    #     self.assertEqual(self.product_1.seller_price, 96)

    # def test_product_seller_price_with_currency(self):
    #     self.po.currency_id = self.env.ref("base.EUR")
    #     usd = self.env.ref("base.USD")
    #     usd.rate_ids[1:].unlink()
    #     usd.rate_ids.name = self.po.date_order.date()
    #     usd.rate_ids.rate = 2
    #     self.assertEqual(self.product_1.seller_price, 5)
    #     self.product_1.qty_to_process = 10.0
    #     self.assertEqual(self.product_1.seller_price, 4)
    #     self.product_1.quick_uom_id = self.uom_dozen
    #     self.assertEqual(self.product_1.seller_price, 48)

    # def test_quick_line_add_1(self):
    #     """
    #     set non-null quantity to any product with no PO line:
    #       -> a new PO line is created with that quantity
    #     """
    #     line_1, line_2 = self.po.order_line
    #     self.assertAlmostEqual(line_1.product_uom_qty, 5.0)
    #     self.assertAlmostEqual(line_1.price_unit, 10)
    #     self.assertAlmostEqual(line_2.product_uom_qty, 6.0)
    #     self.assertAlmostEqual(line_2.price_unit, 5)

    # def test_quick_line_add_2(self):
    #     """
    #     same as previous, but include a different UoM as well
    #     We duplicate _setUpBasicSaleOrder except we ~simultaneously~
    #     write on qty_to_process as well as quick_uom_id
    #     (we want to make sure to test _inverse function when it is triggered twice)
    #     """
    #     vals = {"partner_id": self.partner.id}
    #     if hasattr(self.env["purchase.order"], "order_type"):
    #         vals["order_type"] = self.env.ref("purchase_order_type.po_type_blanket").id
    #     po = self.env["purchase.order"].create(vals)
    #     with Form(po, "purchase.purchase_order_form") as po_form:
    #         po_form.partner_id = self.partner
    #     ctx = {"parent_id": self.po.id, "parent_model": "purchase.order"}
    #     self.product_1 = self.product_1.with_context(**ctx)
    #     self.product_2 = self.product_2.with_context(**ctx)
    #     self.product_1.write({"qty_to_process": 5.0, "quick_uom_id": self.uom_unit.id})
    #     self.product_2.write({"qty_to_process": 6.0, "quick_uom_id": self.uom_dozen.id})

    #     line_1, line_2 = self.po.order_line
    #     self.assertAlmostEqual(line_1.product_uom_qty, 5.0)
    #     self.assertAlmostEqual(line_1.product_qty, 5.0)
    #     self.assertEqual(line_1.product_uom, self.uom_unit)
    #     self.assertAlmostEqual(line_1.price_unit, 10)

    #     self.assertAlmostEqual(line_2.product_uom_qty, 72.0)  # 12 * 6
    #     self.assertAlmostEqual(line_2.product_qty, 6.0)
    #     self.assertEqual(line_2.product_uom, self.uom_dozen)
    #     self.assertAlmostEqual(line_2.price_unit, 48)  # 12 * 4

    # def test_quick_line_update_1(self):
    #     """
    #     set non-null quantity to any product with an already existing PO line:
    #       -> same PO line is updated with that quantity
    #     """
    #     self.product_1.qty_to_process = 7.0
    #     self.product_2.qty_to_process = 13.0
    #     line_1, line_2 = self.po.order_line
    #     self.assertAlmostEqual(line_1.product_qty, 7.0)
    #     self.assertAlmostEqual(line_1.price_unit, 10.0)
    #     self.assertAlmostEqual(line_2.product_qty, 13.0)
    #     self.assertAlmostEqual(line_2.price_unit, 4.0)

    # def test_quick_line_update_2(self):
    #     """
    #     same as previous update only UoM in isolation, not qty
    #     """
    #     self.product_1.quick_uom_id = self.uom_dozen
    #     self.product_2.quick_uom_id = self.uom_unit
    #     line_1, line_2 = self.po.order_line

    #     self.assertEqual(line_1.product_uom, self.uom_dozen)
    #     self.assertAlmostEqual(line_1.product_qty, 5.0)
    #     self.assertAlmostEqual(line_1.product_uom_qty, 60.0)
    #     self.assertAlmostEqual(line_1.price_unit, 96)

    #     self.assertEqual(line_2.product_uom, self.uom_unit)
    #     self.assertAlmostEqual(line_2.product_qty, 6.0)
    #     self.assertAlmostEqual(line_2.product_uom_qty, 6.0)
    #     self.assertAlmostEqual(line_2.price_unit, 5.0)

    # def test_quick_line_update_3(self):
    #     """
    #     same as previous 2 tests combined: we do simultaneous qty + uom updates
    #     """
    #     self.product_1.qty_to_process = 7.0
    #     self.product_2.qty_to_process = 13.0
    #     self.product_1.quick_uom_id = self.uom_dozen
    #     self.product_2.quick_uom_id = self.uom_unit

    #     line_1, line_2 = self.po.order_line
    #     self.assertEqual(line_1.product_uom, self.uom_dozen)
    #     self.assertEqual(line_2.product_uom, self.uom_unit)

    #     self.assertEqual(line_1.product_uom, self.uom_dozen)
    #     self.assertAlmostEqual(line_1.product_qty, 7.0)
    #     self.assertAlmostEqual(line_1.product_uom_qty, 84.0)
    #     self.assertAlmostEqual(line_1.price_unit, 96)

    #     self.assertEqual(line_2.product_uom, self.uom_unit)
    #     self.assertAlmostEqual(line_2.product_qty, 13.0)
    #     self.assertAlmostEqual(line_2.product_uom_qty, 13.0)
    #     self.assertAlmostEqual(line_2.price_unit, 4.0)

    # def test_quick_line_delete(self):
    #     """
    #     set null quantity to any product with existing PO line:
    #       -> PO line is deleted
    #     """
    #     self.product_1.qty_to_process = 0.0
    #     self.product_2.qty_to_process = 0.0
    #     self.assertEqual(len(self.po.order_line), 0)

    # def test_open_quick_view(self):
    #     """
    #     Test that the "Add" button opens the right action
    #     """
    #     product_act_from_po = self.po.add_product()
    #     self.assertEqual(product_act_from_po["type"], "ir.actions.act_window")
    #     self.assertEqual(product_act_from_po["res_model"], "product.product")
    #     self.assertEqual(product_act_from_po["view_mode"], "tree")
    #     self.assertEqual(product_act_from_po["target"], "current")
    #     self.assertEqual(
    #         product_act_from_po["view_id"][0],
    #         self.env.ref("purchase_quick.product_tree_view4purchase").id,
    #     )
    #     self.assertEqual(product_act_from_po["context"]["parent_id"], self.po.id)

    # def test_several_po_for_one_product(self):
    #     """
    #     Test that when we try to mass add a product that already has
    #     several lines with the same product we get a raise
    #     """
    #     self.po.order_line[0].copy()
    #     with self.assertRaises(ValidationError):
    #         self.product_1.qty_to_process = 3.0

    # def test_no_pricelist_for_the_min_qty(self):
    #     """
    #     Checks that if you enter a qty_to_process lower than the seller's min_qty,
    #     the price_unit in de pusrchase.order.line is the standard_price.
    #     """
    #     po = self.env["purchase.order"].create({"partner_id": self.partner.id})
    #     ctx = {
    #         "parent_id": po.id,
    #         "parent_model": "purchase.order",
    #         "quick_access_rights_purchase": 1,
    #     }
    #     product_3 = self.env.ref("product.product_product_5")
    #     self._add_seller(product_3, [(5, 5), (10, 1)])
    #     product_3 = product_3.with_context(**ctx)
    #     product_3.write({"qty_to_process": 1.0, "quick_uom_id": self.uom_unit.id})
    #     line_1 = po.order_line
    #     self.assertEqual(line_1.product_qty, 1.0)
    #     self.assertEqual(line_1.product_uom, self.uom_unit)
    #     self.assertEqual(line_1.price_unit, product_3.standard_price)
