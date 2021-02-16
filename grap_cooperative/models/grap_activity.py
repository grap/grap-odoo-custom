# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class GrapActivity(models.Model):
    _name = "grap.activity"
    _description = "GRAP Activities"

    _inherits = {"grap.member": "grap_member_id"}
    _order = "activity_name"

    _GRAP_ACTIVITY_STATE = [
        ("draft", "No linked"),
        ("progress", "In progress"),
        ("validated", "Validated"),
        ("working", "Working"),
        ("obsolete", "Exited"),
    ]

    # Columns section
    grap_member_id = fields.Many2one(
        string="Member",
        comodel_name="grap.member",
        required=True,
        ondelete="cascade",
    )

    activity_name = fields.Char(string="Activity Name", required=True)

    complete_name = fields.Char(
        string="Complete Name", compute="_compute_complete_name",
        store=True)

    code = fields.Char(string="Code")

    siret = fields.Char(string="SIRET")

    vat = fields.Char(string="Taxe ID")

    web_site = fields.Char(string="Web Site")

    state = fields.Selection(
        string="State",
        selection=_GRAP_ACTIVITY_STATE,
        required=True,
        default="draft",
    )

    type_id = fields.Many2one(string="Type", comodel_name="grap.type")

    accountant_interlocutor_id = fields.Many2one(
        string="Accoutant", comodel_name="grap.people"
    )

    hr_interlocutor_id = fields.Many2one(
        string="HR Interlocutor", comodel_name="grap.people"
    )

    attendant_interlocutor_id = fields.Many2one(
        string="Attendant", comodel_name="grap.people"
    )

    category_ids = fields.Many2many(
        string="Categories",
        comodel_name="grap.category",
        relation="grap_activity_category_rel",
        column1="activity_id",
        column2="category_id",
    )

    people_ids = fields.One2many(
        string="Workers",
        comodel_name="grap.activity.people",
        inverse_name="activity_id",
    )

    @api.depends("code", "activity_name")
    def _compute_complete_name(self):
        for activity in self:
            activity.complete_name = "{} - {}".format(
                activity.code, activity.activity_name)

    # Overloads section
    @api.model
    def create(self, vals):
        vals["name"] = vals["activity_name"]
        return super().create(vals)

    def write(self, vals):
        if "activity_name" in vals.keys():
            vals["name"] = vals["activity_name"]
        return super().write(vals)

    def unlink(self):
        members = self.mapped("grap_member_id")
        res = super().unlink()
        members.unlink()
        return res
