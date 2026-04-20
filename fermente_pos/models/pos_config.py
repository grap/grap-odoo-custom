# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class PosConfig(models.Model):
    _inherit = "pos.config"

    def _default_sale_journal(self):
        return self._default_invoice_journal()
