# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
import odoo.addons.decimal_precision as dp


class WizardUpdateInvoiceSupplierinfoLine(models.TransientModel):
    _inherit = "wizard.update.invoice.supplierinfo.line"

    current_standard_price = fields.Float(
        digits=dp.get_precision("GRAP Cost Price")
    )

    new_standard_price = fields.Float(
        digits=dp.get_precision("GRAP Cost Price")
    )

    current_price = fields.Float(
        digits=dp.get_precision("GRAP Purchase Price Unit")
    )

    new_price = fields.Float(
        digits=dp.get_precision("GRAP Purchase Price Unit")
    )
