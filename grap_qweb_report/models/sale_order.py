# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "report.custom.message.mixin"]

    price_unit_include_taxes = fields.Boolean(
        string="Subtotal w / wo taxes",
        compute="_compute_price_unit_include_taxes",
        default=False,
    )

    def action_invoice_create(self, grouped=False, final=False):
        if not grouped and len(self) > 1:
            return super(
                SaleOrder, self.with_context(add_picking_date=True)
            ).action_invoice_create(grouped=grouped, final=final)
        return super().action_invoice_create(grouped=grouped, final=final)

    @api.depends("fiscal_position_id")
    def _compute_price_unit_include_taxes(self):
        # Check if fiscal_position is w ou wo taxes (just checking first line)
        for invoice in self:
            # Check if there is a fiscal_position
            try:
                tax_dest = invoice.fiscal_position_id.tax_ids[0].tax_dest_id
            # No fiscal position → wo taxes
            except IndexError:
                invoice.price_unit_include_taxes = False
            else:
                if tax_dest.price_include:
                    invoice.price_unit_include_taxes = True
                else:
                    invoice.price_unit_include_taxes = False
