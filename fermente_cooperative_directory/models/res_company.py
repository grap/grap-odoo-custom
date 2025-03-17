# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    complete_address = fields.Char(compute="_compute_complete_address")

    worker_ids = fields.One2many(
        string="Workers",
        comodel_name="hr.employee.global",
        inverse_name="company_id",
    )

    is_displayed_in_directory = fields.Boolean(
        string="Displayed in Directory", default=True
    )

    cooperative_joining_date = fields.Date(
        help="Date of the commission in which the cooperative"
        " accepted the entry of this activity"
    )

    # Interlocutors in Service Team
    accounting_interlocutor_id = fields.Many2one(
        string="Accounting Interlocutor", comodel_name="hr.employee.global"
    )

    hr_interlocutor_id = fields.Many2one(
        string="HR Interlocutor", comodel_name="hr.employee.global"
    )

    attendant_interlocutor_id = fields.Many2one(
        string="Attendant Interlocutor", comodel_name="hr.employee.global"
    )

    def _compute_complete_address(self):
        for company in self:
            company.complete_address = company.partner_id._display_address(
                without_company=True
            )
