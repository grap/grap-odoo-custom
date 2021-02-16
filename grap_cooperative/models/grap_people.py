# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class GrapPeople(models.Model):
    _name = "grap.people"
    _description = "GRAP Peoples"

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

    activity_description = fields.Char(
        string="Activities Description",
        compute="_compute_activity_description",
        store=True,
    )

    mandate_ids = fields.Many2many(
        string="Mandates",
        comodel_name="grap.mandate",
        relation="grap_people_mandate_rel",
        column1="people_id",
        column2="mandate_id",
    )

    is_birthday = fields.Boolean(string="Is Birthday", compute="_compute_is_birthday")

    # Compute section
    @api.model
    def _get_name(self, firstName, lastName):
        return lastName + " " + firstName

    @api.depends("activity_ids")
    def _compute_activity_description(self):
        for people in self:
            people.activity_description = ", ".join(
                people.mapped("activity_ids.activity_id.name")
            )

    @api.depends("birthdate")
    def _compute_is_birthday(self):
        for people in self.filtered(lambda x: x.birthdate):
            now = datetime.now().date()
            birthdate = people.birthdate.replace(year=now.year)
            delta = birthdate - now
            if delta.days >= -1 and delta.days < 2:
                people.is_birthday = True

    # Overloads section
    @api.model
    def create(self, vals):
        vals["name"] = self._get_name(vals["first_name"], vals["last_name"])
        return super().create(vals)

    def write(self, vals):
        if "last_name" in vals.keys() or "first_name" in vals.keys():
            if len(self) > 1:
                raise UserError(_("Unable to perform name changes on many people"))
            vals["name"] = self._get_name(
                vals.get("first_name", self.first_name),
                vals.get("last_name", self.last_name),
            )
        return super().write(vals)

    def unlink(self):
        members = self.mapped("grap_member_id")
        res = super().unlink()
        members.unlink()
        return res
