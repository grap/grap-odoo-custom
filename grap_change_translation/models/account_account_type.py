# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    name = fields.Char(translate=False)

    vat_label = fields.Char(translate=False)
