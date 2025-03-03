# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestFoodMenuWizardProduction(TransactionCase):
    def setUp(self):
        super().setUp()
        self.bom_desk = self.env.ref("mrp.mrp_bom_desk")
        self.food_menu_french = self.env.ref(
            "mrp_food_menu.demo_menu_french_revolution"
        )
        self.wizard_obj = self.env["bom.wizard.production"]
        self.wizard = self.wizard_obj.with_context(
            active_ids=[self.food_menu_french.id],
            active_model="mrp.food.menu",
        ).create({})

    def test_01_check_wizard_food_menu_description(self):
        new_note = "Nice office to work on overturning capitalism"
        self.food_menu_french.internal_notes = new_note
        self.wizard2 = self.wizard_obj.with_context(
            active_ids=[self.food_menu_french.id],
            active_model="mrp.food.menu",
        ).create({})
        # import pdb; pdb.set_trace()
        self.assertEqual(self.wizard2.notes_for_pdf, new_note)

    def test_02_report_bom_wizard_check_default(self):
        data = self.wizard._prepare_data()
        # Check default values
        self.assertEqual(data["option_group_by_product_category"], True)
        self.assertEqual(data["option_print_bom"], False)
        self.assertEqual(data["option_production_date"], False)

    def test_03_report_bom_wizard(self):
        data = self.wizard._prepare_data()
        # Check purchase cost
        report_obj = self.env[
            "report.mrp_bom_wizard_production.report_bom_wizard_production"
        ]
        values = report_obj._get_report_values(0, data)
        self.assertEqual(values["purchase_total_cost"], 249.6)
