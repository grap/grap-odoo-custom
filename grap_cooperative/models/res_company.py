# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    clean_name = fields.Char(
        string="Clean name",
        compute="_compute_clean_name",
        store=True,
    )

    people_ids = fields.One2many(
        string="Workers",
        comodel_name="grap.people",
        inverse_name="company_id",
    )

    manager_ids = fields.Many2many(
        string="Co-directors",
        comodel_name="grap.people",
        relation="grap_people_companies_managers_rel",
        column1="company_manager_id",
        column2="people_id",
    )

    # Cooperative informations
    state_id = fields.Many2one(
        string="State",
        comodel_name="res.country.state",
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

    # Interlocutors in company
    accounting_interlocutor_activity_id = fields.Many2one(
        string="Accouting contact person", comodel_name="grap.people"
    )

    hr_interlocutor_activity_id = fields.Many2one(
        string="HR contact person", comodel_name="grap.people"
    )

    it_interlocutor_activity_id = fields.Many2one(
        string="IT contact person", comodel_name="grap.people"
    )

    # Interlocutors in service team
    accounting_interlocutor_service_id = fields.Many2one(
        string="Accouting contact in service team", comodel_name="grap.people"
    )

    hr_interlocutor_service_id = fields.Many2one(
        string="HR contact person in service team", comodel_name="grap.people"
    )

    it_interlocutor_service_id = fields.Many2one(
        string="IT contact person in service team", comodel_name="grap.people"
    )

    attendant_interlocutor_service_id = fields.Many2one(
        string="Attendant contact person in service team", comodel_name="grap.people"
    )

    @api.depends("name")
    def _compute_clean_name(self):
        for company in self:
            company.clean_name = (company.name or "").replace("|", "")

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
