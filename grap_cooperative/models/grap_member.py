# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools


class GrapMember(models.Model):
    _name = "grap.member"
    _description = "GRAP Members"

    _order = "name"

    # Columns section
    name = fields.Char(string="Name", readonly=True)

    image = fields.Binary(string="Image", attachment=True)

    image_medium = fields.Binary(string="Medium-sized image", attachment=True)

    image_small = fields.Binary(string="Small-sized image", attachment=True)

    street = fields.Char(string="Street")

    zip = fields.Char(string="Zip")

    city = fields.Char(string="City")

    working_email = fields.Char(string="Contact Email")

    working_phone = fields.Char(string="Working Phone")

    college_id = fields.Many2one(string="College", comodel_name="grap.college")

    # Overload section
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            tools.image_resize_images(vals, sizes={"image": (1024, None)})
        return super().create(vals_list)

    def write(self, vals):
        tools.image_resize_images(vals, sizes={"image": (1024, None)})
        return super().write(vals)
