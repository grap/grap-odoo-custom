# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class GrapPeople(models.Model):
    _name = "grap.people"
    _inherits = {"grap.member": "grap_member_id"}
    _order = "last_name,first_name"

    # Column section
    grap_member_id = fields.Many2one(
        comodel_name="grap.member",
        string="Member",
        required=True,
        ondelete="cascade",
    )

    first_name = fields.Char(string="First name", required=True)

    last_name = fields.Char(string="Last name", required=True)

    birthdate = fields.Date("Birthdate")

    private_phone = fields.Char(string="Private Phone")

    activity_ids = fields.One2many(
        string="Activities",
        comodel_name="grap.activity.people",
        inverse_name="people_id",
    )

    accountant_activity_ids = fields.One2many(
        string="Accounting Performed for Activities",
        comodel_name="grap.activity",
        inverse_name="accountant_interlocutor_id",
    )

    hr_activity_ids = fields.One2many(
        string="Human Ressources Performed for Activities",
        comodel_name="grap.activity",
        inverse_name="hr_interlocutor_id",
    )

    attendant_activity_ids = fields.One2many(
        string="Attending Performed for Activities",
        comodel_name="grap.activity",
        inverse_name="attendant_interlocutor_id",
    )

    mandate_ids = fields.Many2many(
        string="Mandates",
        comodel_name="grap.mandate",
        relation="grap_people_mandate_rel",
        column1="people_id",
        column2="mandate_id",
    )

    description = fields.Text(string="Self Description")

    skills = fields.Text(string="Skills")

    is_birthday = fields.Boolean(compute="_compute_is_birthday_color")

    color = fields.Integer(compute="_compute_is_birthday_color")

    # Compute section
    @api.model
    def _get_name(self, firstName, lastName):
        return lastName + " " + firstName

    @api.multi
    def _compute_is_birthday_color(self):
        for people in self.filtered(lambda x: x.birthdate):
            now = datetime.now()
            birthdate = datetime.strptime(
                people.birthdate, "%Y-%m-%d"
            ).replace(year=now.year)
            delta = birthdate - now
            if delta.days >= -1 and delta.days < 2:
                people.is_birthday = True
                people.color = 4

    # Overloads section
    @api.model
    def create(self, vals):
        vals["name"] = self._get_name(vals["first_name"], vals["last_name"])
        return super(GrapPeople, self).create(vals)

    @api.multi
    def write(self, vals):
        if "last_name" in vals.keys() or "first_name" in vals.keys():
            if len(self) > 1:
                raise UserError(
                    _("Unable to perform name changes on many people")
                )
            vals["name"] = self._get_name(
                vals.get("first_name", self.first_name),
                vals.get("last_name", self.last_name),
            )
        return super(GrapPeople, self).write(vals)
