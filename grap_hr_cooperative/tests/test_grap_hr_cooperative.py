# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestCreateEmployee(TransactionCase):

    def setUp(self):
        super(TestCreateEmployee, self).setUp()
        self.coop_people = self.env["grap.people"]
        self.people_SLG = self.env.ref(
            "grap_cooperative.people_SLG"
        )
        self.people_QD = self.env.ref(
            "grap_cooperative.people_QD"
        )

    # Test Section
    def test_01_create_employee(self):
        # Create employee from coop people
        employee = self.people_SLG.create_employee_from_coop_people(edit=False)
        self.assertEqual(employee.name, self.people_SLG.name)
        self.assertEqual(employee.worker_activity.id,
                         self.people_SLG.activity_ids[0].activity_id.id)
        self.assertEqual(employee.work_email, self.people_SLG.working_email)
        self.assertEqual(employee.work_phone, self.people_SLG.working_phone)
        self.assertEqual(employee.birthday, self.people_SLG.birthdate)
