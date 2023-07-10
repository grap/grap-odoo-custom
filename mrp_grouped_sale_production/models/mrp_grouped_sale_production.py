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
    # End Matrix 2D

    mrp_production_ids = fields.One2many(
        comodel_name="mrp.production", compute="_compute_mrp_production_ids"
    )

    mrp_production_qty = fields.Integer(
        compute="_compute_production_qty",
    )

    @api.depends("order_ids")
    def _compute_orders_qty(self):
        for mrp_grouped_sale_prod in self:
            mrp_grouped_sale_prod.orders_qty = len(mrp_grouped_sale_prod.order_ids)

    @api.depends("order_ids")
    def _compute_mrp_production_ids(self):
        for grouped_prod in self:
            # production_ids is a sale_mrp_link field
            grouped_prod.mrp_production_ids = grouped_prod.order_ids.mapped(
                "production_ids"
            )

    @api.depends("mrp_production_ids")
    def _compute_production_qty(self):
        for grouped_prod in self:
            grouped_prod.mrp_production_qty = len(grouped_prod.mrp_production_ids)

    @api.multi
    def action_view_production(self):
        action = self.env.ref("mrp.mrp_production_action").read()[0]
        if self.mrp_production_qty > 1:
            action["domain"] = [("id", "in", self.mrp_production_ids.ids)]
        else:
            action["views"] = [
                (self.env.ref("mrp.mrp_production_form_view").id, "form")
            ]
            action["res_id"] = self.mrp_production_ids.id
        return action
