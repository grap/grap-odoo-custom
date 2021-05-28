# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    display_name = fields.Char(
        string="Clean name",
        compute="_compute_display_name",
    )

    people_ids = fields.One2many(
        string="Workers",
        comodel_name="grap.people",
        inverse_name="company_id",
    )

    manager_ids = fields.Many2many(
        string="Workers with mandates",
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

    accounting_closing_date = fields.Date(
        string="Accounting closure",
    )

    is_using_Odoo = fields.Boolean(
        string="Is using Odoo",
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

    @api.depends("name")
    def _compute_display_name(self):
        for activity in self:
            if activity.name:
                activity.display_name = activity.name.replace("|", "")

    @api.depends("street", "city", "zip")
    def _compute_clean_adress(self):
        for activity in self:
            activity.clean_address = ""
            if activity.street:
                activity.clean_address += activity.street + ", "
            if activity.zip:
                activity.clean_address += activity.zip + " "
            if activity.city:
                activity.clean_address += activity.city.upper()

    # manager_ids = fields.Many2many(
    #     string="Workers with mandates",
    #     comodel_name="grap.people",
    #     inverse_name="company_mandate_id")
    # compute='_get_people_with_mandates')

    # def _get_people_with_mandates(self):
    #     self.people_with_mandates = self.people_ids.search(
    #         [('mandate_ids', '!=', False),
    #          ('company_id', '=', self.id)
    #         ])

    # complete_name = fields.Char(
    #     string="Complete Name", compute="_compute_complete_name", store=True
    # )

    # @api.depends("code", "name")
    # def _compute_complete_name(self):
    #     for activity in self:
    #         _name = self.name
    #         if activity.name:
    #             _name = self.name.replace('|', '')
    #         activity.complete_name = "{} - {}".format(
    #             activity.code, activity._name
    #         )
