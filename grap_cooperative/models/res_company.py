# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    map_display_address = fields.Char(compute="_compute_map_display_address")

    people_ids = fields.One2many(
        string="Workers",
        comodel_name="grap.people",
        inverse_name="company_id",
    )

    clean_address = fields.Char(
        string="Clean address",
        compute="_compute_clean_adress",
    )

    is_using_odoo = fields.Boolean(
        string="Is using Odoo",
    )

    is_displayed_in_directory = fields.Boolean(
        string="Displayed in Directory", default=True
    )

    cooperative_joining_date = fields.Date(
        help="Date of the commission in which the cooperative"
        " accepted the entry of this activity"
    )

    # Referents in Company
    accounting_referent_id = fields.Many2one(
        string="Accounting Referent", comodel_name="grap.people"
    )

    hr_referent_id = fields.Many2one(string="HR Referent", comodel_name="grap.people")

    it_referent_id = fields.Many2one(string="IT Referent", comodel_name="grap.people")

    communication_referent_id = fields.Many2one(
        string="Communication Referent", comodel_name="grap.people"
    )

    # Interlocutors in Service Team
    accounting_interlocutor_id = fields.Many2one(
        string="Accounting Interlocutor", comodel_name="grap.people"
    )

    hr_interlocutor_id = fields.Many2one(
        string="HR Interlocutor", comodel_name="grap.people"
    )

    attendant_interlocutor_id = fields.Many2one(
        string="Attendant Interlocutor", comodel_name="grap.people"
    )

    @api.depends("street", "city", "zip")
    def _compute_clean_adress(self):
        for company in self:
            company.clean_address = ""
            if company.street:
                company.clean_address += company.street + ", "
            if company.zip:
                company.clean_address += company.zip + " "
            if company.city:
                company.clean_address += company.city.upper()

    def _compute_map_display_address(self):
        for company in self:
            company.map_display_address = company.partner_id._display_address(
                without_company=True
            )
