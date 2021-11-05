# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice", "report.custom.message.mixin"]
