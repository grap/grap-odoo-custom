# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpGroupedSaleProduction(models.Model):
    _name = "mrp.grouped.sale.production"
    _description = "Grouped Sale and Production"

    name = fields.Char()
    production_date = fields.Date()
    note = fields.Char()

    orders_qty = fields.Integer(
        "Sale Order Quantity",
        compute="_compute_orders_qty",
        help="Number of Sales associated in the grouped Sale Production",
    )

    # Matrix 2d
    order_ids = fields.One2many(
        string="Sales Orders",
        comodel_name="sale.order",
        inverse_name="grouped_order_id",
    )

    @api.depends("order_ids")
    def _compute_orders_qty(self):
        for mrp_grouped_sale_prod in self:
            mrp_grouped_sale_prod.orders_qty = len(mrp_grouped_sale_prod.order_ids)
