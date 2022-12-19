# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice", "report.custom.message.mixin"]


    price_unit_include_taxes = fields.Boolean(
        string="Price Unit (w / wo taxes)",
        compute="_compute_price_unit_include_taxes",
        default=False,
    )

    @api.depends("fiscal_position_id")
    def _compute_price_unit_include_taxes(self):
        # Check if fiscal_position is w ou wo taxes (just checking first line)
        # Default : no fiscal position → no taxes
        self.price_unit_include_taxes = False
        for invoice in self.filtered(lambda x: x.fiscal_position_id.tax_ids):
            if invoice.fiscal_position_id.tax_ids[0].tax_dest_id.price_include:
                invoice.price_unit_include_taxes = True
            else:
                invoice.price_unit_include_taxes = False
