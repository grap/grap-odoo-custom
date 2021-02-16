# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class GrapActivityPeople(models.Model):
    _name = "grap.activity.people"
    _description = "GRAP Activity - People"

    _order = "people_id"

    # Columns section
    activity_id = fields.Many2one(
        string="Activity",
        comodel_name="grap.activity",
        required=True,
        ondelete="cascade",
        readonly=True,
    )

    people_id = fields.Many2one(
        string="People",
        comodel_name="grap.people",
        required=True,
        ondelete="cascade",
    )

    function = fields.Char(string="Function")

    people_name = fields.Char(
        string="People Name",
        related="people_id.name",
        readonly=True,
    )

    people_image_small = fields.Binary(
        string="People Small-sized image", related="people_id.image_small"
    )

    people_working_email = fields.Char(
        string="Contact Email",
        related="people_id.working_email",
        readonly=True,
    )

    people_private_phone = fields.Char(
        string="Private Phone",
        related="people_id.private_phone",
        readonly=True,
    )

    people_working_phone = fields.Char(
        string="Working Phone",
        related="people_id.grap_member_id.working_phone",
        readonly=True,
    )

    # Constraints section
    _sql_constraints = [
        (
            "activity_people_uniq",
            "unique(activity_id, people_id)",
            "A people can work only once time in an activity!",
        ),
    ]
