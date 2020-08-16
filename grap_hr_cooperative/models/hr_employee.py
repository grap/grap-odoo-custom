# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    # Columns Section
    worker_activity = fields.Many2one(
        string="Activity",
        comodel_name="grap.activity",
        required=True,
        help="Worker activity",
    )

    coop_people = fields.One2many(
        comodel_name="grap.people",
        inverse_name="emp_id",
        string="Coop people",
    )
