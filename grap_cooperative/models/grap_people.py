# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo import api, fields, models, tools


class GrapPeople(models.Model):
    _name = "grap.people"
    _description = "GRAP Peoples"

    _order = "name"

    # Columns section
    name = fields.Char(string="Full name", required=True, store=True)

    first_name = fields.Char(string="First name", required=True)

    last_name = fields.Char(string="Last name", required=True)

    pronouns = fields.Char(string="Pronoun(s)")

    image = fields.Binary(string="Image", attachment=True)

    image_medium = fields.Binary(string="Medium-sized image", attachment=True)

    image_small = fields.Binary(string="Small-sized image", attachment=True)

    street = fields.Char(string="Street")

    zip = fields.Char(string="Zip")

    city = fields.Char(string="City")

    profession = fields.Char(string="Profession")

    working_email = fields.Char(string="Working Email")

    working_phone = fields.Char(string="Working Phone")

    birthdate = fields.Date("Birthdate")

    is_birthday = fields.Boolean(string="Is Birthday", compute="_compute_is_birthday")

    private_phone = fields.Char(string="Private Phone")

    college_id = fields.Many2one(string="College", comodel_name="grap.college")

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        inverse_name="people_ids",
        domain="[('is_displayed_in_directory', '=', True)]",
        context={
            "form_view_ref": "grap_cooperative.view_res_company_form_directory",
            "tree_view_ref": "grap_cooperative.view_res_company_tree_directory",
        },
    )

    company_code = fields.Char(related="company_id.code", store=True)

    company_manager_ids = fields.Many2many(
        string="Companies with mandates",
        comodel_name="res.company",
        relation="grap_people_companies_managers_rel",
        column1="people_id",
        column2="company_manager_id",
    )

    mandate_ids = fields.Many2many(
        string="Cooperative mandates",
        comodel_name="grap.mandate",
        relation="grap_people_mandate_rel",
        column1="people_id",
        column2="mandate_id",
    )

    @api.depends("birthdate")
    def _compute_is_birthday(self):
        for people in self.filtered(lambda x: x.birthdate):
            now = datetime.now().date()
            birthdate = people.birthdate.replace(year=now.year)
            delta = birthdate - now
            if delta.days >= -1 and delta.days < 2:
                people.is_birthday = True

    # Set people name with first and last name
    # Optimize for creating people directly from company form
    @api.onchange("first_name", "last_name")
    def _handle_name(self):
        for people in self:
            if people.name and not people.first_name and not people.last_name:
                split_name = people.name.split()
                if len(split_name) > 0:
                    people.first_name = split_name[0]
                if len(split_name) > 1:
                    people.last_name = " ".join(split_name[1:])
            else:
                people.name = ""
                if people.last_name:
                    people.last_name = people.last_name.upper()
                    people.name = people.last_name
                if people.first_name:
                    people.first_name = people.first_name.capitalize()
                    people.name += " " + people.first_name

    # Overloads section
    @api.model
    def create(self, vals):
        tools.image_resize_images(vals, sizes={"image": (1024, None)})
        return super().create(vals)

    def write(self, vals):
        tools.image_resize_images(vals, sizes={"image": (1024, None)})
        return super().write(vals)

    def detach_people_from_company(self):
        self.write({"company_id": False})
