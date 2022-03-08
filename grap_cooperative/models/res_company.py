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

    # Referents in Company
    accounting_referent_id = fields.Many2one(
        string="Accouting Referent", comodel_name="grap.people"
    )

    hr_referent_id = fields.Many2one(string="HR Referent", comodel_name="grap.people")

    it_referent_id = fields.Many2one(string="IT Referent", comodel_name="grap.people")

    # Interlocutors in Service Team
    accounting_interlocutor_id = fields.Many2one(
        string="Accouting Interlocutor", comodel_name="grap.people"
    )

    hr_interlocutor_id = fields.Many2one(
        string="HR Interlocutor", comodel_name="grap.people"
    )

    it_interlocutor_id = fields.Many2one(
        string="IT Interlocutor", comodel_name="grap.people"
    )

    attendant_interlocutor_id = fields.Many2one(
        string="Attendant Interlocutor", comodel_name="grap.people"
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
