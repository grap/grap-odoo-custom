# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountProductFiscalClassificationTemplate(models.Model):
    _inherit = "account.product.fiscal.classification.template"

    name = fields.Char(translate=False)
