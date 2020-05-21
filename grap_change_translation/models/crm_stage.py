# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class CrmStage(models.Model):
    _inherit = "crm.stage"

    legend_priority = fields.Text(translate=False)

    name = fields.Char(translate=False)
