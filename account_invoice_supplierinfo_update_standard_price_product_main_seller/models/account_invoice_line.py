# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def _prepare_supplier_wizard_line(self, supplierinfo):
        self.ensure_one()
        res = super()._prepare_supplier_wizard_line(supplierinfo)
        res["is_line_main_seller_price"] = (
            supplierinfo and supplierinfo.is_main_seller or False
        )
        return res
