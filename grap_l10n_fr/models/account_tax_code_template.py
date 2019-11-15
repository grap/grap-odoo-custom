# Copyright (C) 2018-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountTaxCodeTemplate(models.Model):
    _inherit = "account.tax.code.template"

    active = fields.Boolean(string="active", default=True)

    ebp_suffix = fields.Char(
        "Tax Codes suffix in EBP",
        size=4,
        oldname="ref_nb",
        help="When exporting Entries to EBP, this suffix will be"
        " appended to the Account Number to make it a new Account.",
    )
