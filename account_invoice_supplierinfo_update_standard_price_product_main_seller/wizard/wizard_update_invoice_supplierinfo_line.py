# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class WizardUpdateInvoiceSupplierinfoLine(models.TransientModel):
    _inherit = "wizard.update.invoice.supplierinfo.line"

    is_line_main_seller_price = fields.Boolean(
        string="Main seller",
        readonly=True,
    )
    is_line_main_seller_price_icon = fields.Char(string="Main seller", default="🥇")

    def _prepare_supplierinfo_update(self):
        res = super()._prepare_supplierinfo_update()
        # Arbitrarily we set a big sequence for this supplier info
        # not to be in sequence=1 and be falsely main seller
        res["sequence"] = 100
        return res
