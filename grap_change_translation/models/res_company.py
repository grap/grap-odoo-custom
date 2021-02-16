# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    overdue_msg = fields.Text(translate=False)

    report_footer = fields.Text(translate=False)

    rml_footer = fields.Text(translate=False)

    sale_note = fields.Text(translate=False)
