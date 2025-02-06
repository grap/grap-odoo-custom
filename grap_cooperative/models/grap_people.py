# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo import api, fields, models


class GrapPeople(models.Model):
    _name = "grap.people"
    _description = "GRAP Peoples"

    _order = "first_name, last_name"

    first_name = fields.Char(required=True)

    last_name = fields.Char(required=True)

    image = fields.Binary(attachment=True)

    image_medium = fields.Binary(attachment=True)

    image_small = fields.Binary(attachment=True)

    street = fields.Char()

    zip = fields.Char()

    city = fields.Char()

    working_email = fields.Char()

    working_phone = fields.Char()

    birthdate = fields.Date()

    private_phone = fields.Char()

    company_id = fields.Many2one(
        comodel_name="res.company",
        domain="[('is_displayed_in_directory', '=', True)]",
        context={
            "form_view_ref": "grap_cooperative.view_res_company_form_directory",
            "tree_view_ref": "grap_cooperative.view_res_company_tree_directory",
        },
    )

    company_code = fields.Char(related="company_id.code", store=True)
