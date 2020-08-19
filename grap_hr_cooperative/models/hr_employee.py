# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    _HR_EMPLOYEE_STATE = [
        ("to_be_validated", "To be validated"),
        ("necessary_changes", "Necessary Changes"),
        ("validated", "Validated"),
    ]

    _HR_EMPLOYEE_STATE_COLOR = {
        "to_be_validated" : 2, #orange
        "necessary_changes" : 1, #red
        "validated" : 0, #none
    }

    # Columns Section
    worker_activity = fields.Many2one(
        string="Activity",
        comodel_name="grap.activity",
        help="Worker activity",
    )

    coop_people = fields.One2many(
        comodel_name="grap.people",
        inverse_name="emp_id",
        string="Coop people",
    )

    state = fields.Selection(
        string="Emloyee Form State",
        selection=_HR_EMPLOYEE_STATE,
        required=True,
        store=True,
        default="to_be_validated",
    )

    color = fields.Integer(
        string='Color Index',
        compute="_compute_color",
        default=2) #none

    @api.multi
    def employee_change_state(self, state):
        for employee in self:
            employee.state = state

    @api.multi
    def employee_change_state_to_to_be_validated(self):
        for employee in self:
            employee.color = self._HR_EMPLOYEE_STATE_COLOR["to_be_validated"];
            self.employee_change_state('to_be_validated')

    @api.multi
    def employee_change_state_to_necessary_changes(self):
        for employee in self:
            employee.color = self._HR_EMPLOYEE_STATE_COLOR["necessary_changes"];
            self.employee_change_state('necessary_changes')

    @api.multi
    def employee_change_state_to_validated(self):
        for employee in self:
            employee.color = self._HR_EMPLOYEE_STATE_COLOR["validated"];
            self.employee_change_state('validated')

    @api.depends('state')
    def _compute_color(self):
        for employee in self:
            employee.color = self._HR_EMPLOYEE_STATE_COLOR[employee.state];
