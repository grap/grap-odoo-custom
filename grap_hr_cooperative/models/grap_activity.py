# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class GrapActivity(models.Model):
    _inherit = "grap.activity"

    worker_ids = fields.One2many(
        string="Coop Workers",
        comodel_name="hr.employee",
        inverse_name="worker_activity",
    )
