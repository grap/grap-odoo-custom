# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, fields


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    # Column Section
    state = fields.Selection(
        related="invoice_id.state",
        string="State",
        index=True,
        store=True,
        readonly=True,
    )

    date_invoice = fields.Date(
        related="invoice_id.date_invoice",
        string="Date invoice",
        index=True,
        store=True,
        readonly=True,
    )

    categ_id = fields.Many2one(
        related="product_id.categ_id",
        string="Category",
        index=True,
        comodel_name="product.category",
        store=True,
        readonly=True,
    )

    tax_ids_description = fields.Char(
        string="Taxes (Description)", compute="_compute_tax_ids_description",
        store=True
    )

    # Compute Section
    @api.multi
    @api.depends("invoice_line_tax_ids")
    def _compute_tax_ids_description(self):
        for line in self:
            line.tax_ids_description = ",".join(
                [
                    x.description and x.description or x.name
                    for x in line.invoice_line_tax_ids
                ]
            )
