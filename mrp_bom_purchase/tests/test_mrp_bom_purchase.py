# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMrpBomPurchase(TransactionCase):
    def setUp(self):
        super(TestMrpBomPurchase, self).setUp()
        self.bom_desk = self.env.ref("mrp.mrp_bom_desk")

    def test_01_check_wizard_onchange_quantity(self):
        # Create wizard with Table "desk"
        wizard_obj = self.env["bom.print.purchase.list.wizard"]
        wizard = wizard_obj.with_context(active_ids=[self.bom_desk.id]).create({})
        first_line = wizard.line_ids[0]
        line_total = first_line.wizard_line_subtotal
        # Change quantity
        first_line.quantity = first_line.quantity * 3
        first_line._onchange_wizard_line_cost()
        self.assertEqual(first_line.wizard_line_subtotal, line_total * 3)

    def test_02_check_wizard_bom_description(self):
        # Add description in bom
        new_description = "Nice office to work on overturning capitalism"
        self.bom_desk.description_short = new_description
        # Create wizard with Table "desk"
        wizard_obj = self.env["bom.print.purchase.list.wizard"]
        wizard = wizard_obj.with_context(active_ids=[self.bom_desk.id]).create({})
        first_line = wizard.line_ids[0]
        # Check
        self.assertEqual(first_line.bom_description, new_description)