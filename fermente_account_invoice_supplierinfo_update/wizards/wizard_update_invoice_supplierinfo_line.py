# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WizardUpdateInvoiceSupplierinfoLine(models.TransientModel):
    _inherit = "wizard.update.invoice.supplierinfo.line"

    has_uom_different = fields.Boolean(
        compute="_compute_has_uom_different",
    )

    @api.depends("current_uom_id", "new_uom_id")
    def _compute_has_uom_different(self):
        for line in self:
            line.has_uom_different = line.current_uom_id != line.new_uom_id
