# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "name"

    # Columns Section
    valuation_qty_available = fields.Float(
        compute="_compute_valuation_qty_available",
        string="Valuation of Quantity on Hand",
    )

    valuation_virtual_available = fields.Float(
        compute="_compute_valuation_virtual_available",
        string="Valuation of Virtual Quantity",
    )

    # Compute Section
    @api.multi
    def _compute_valuation_qty_available(self):
        for product in self:
            product.valuation_qty_available = (
                product.qty_available * product.standard_price
            )

    @api.multi
    def _compute_valuation_virtual_available(self):
        for product in self:
            product.valuation_virtual_available = (
                product.virtual_available * product.standard_price
            )
