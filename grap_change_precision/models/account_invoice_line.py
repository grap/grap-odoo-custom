# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    purchase_price = fields.Float(
        digits=dp.get_precision("GRAP Cost Price")
    )

    margin = fields.Float(
        digits=dp.get_precision("GRAP Cost Price")
    )

    margin_signed = fields.Float(
        digits=dp.get_precision("GRAP Cost Price")
    )

    price_unit = fields.Float(
        digits=dp.get_precision("GRAP Invoice Price Unit")
    )

    @api.multi
    def _get_unit_price_in_purchase_uom(self):
        # Overwrite this function, to avoid to round the price_unit
        # in the currency of the invoice. without this code
        # it truncate with 2 digits the purchase_price, and
        # in GRAP, the purchase price is 4 digits.
        # the overwrited function is in the module
        # 'account_invoice_supplierinfo_update'
        self.ensure_one()
        if not self.product_id:
            return self.price_unit
        uom = self.uom_id or self.product_id.uom_id
        return uom._compute_price(
            self.price_unit, self.product_id.uom_po_id)
