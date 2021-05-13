# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    list_price = fields.Float(
        track_visibility="onchange",
    )

    uom_po_id = fields.Many2one(
        domain="""[
        ('use_type', 'in', ('purchase', 'both')),
        ('category_id', '=', uom_category_id)
    ]"""
    )

    # Overwrite Section
    @api.multi
    @api.depends("type", "default_invoice_policy")
    def _compute_invoice_policy(self):
        invoice_policy = self.env.context.get("invoice_policy")
        for tmpl in self:
            if tmpl.type == "service":
                tmpl.invoice_policy = "order"
            else:
                if invoice_policy:
                    tmpl.invoice_policy = invoice_policy
                else:
                    tmpl.invoice_policy = "delivery"
