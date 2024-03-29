# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpSaleGrouped(models.Model):
    _name = "mrp.sale.grouped"
    _description = "Grouped Sale Production"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    _SALES_STATE_SELECTION = [
        ("sales_in_progress", "Sales in progress"),
        ("all_sales_confirmed", "Sales confirmed"),
    ]

    _PROD_STATE_SELECTION = [
        ("prod_in_progress", "Production in progress"),
        ("all_production_done", "Production done"),
    ]

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda s: s._default_company_id(),
    )

    name = fields.Char(
        required=True,
    )
    date = fields.Date(
        string="Production date",
        help="For example, it will be used for production wizard PDF.",
    )
    notes = fields.Char()

    sales_state = fields.Selection(
        selection=_SALES_STATE_SELECTION,
        string="Sales State",
        default="sales_in_progress",
        track_visibility=True,
        compute="_compute_sales_state",
    )

    production_state = fields.Selection(
        selection=_PROD_STATE_SELECTION,
        string="Production State",
        default="prod_in_progress",
        track_visibility=True,
        compute="_compute_production_state",
    )

    orders_qty = fields.Integer(
        "Sale Order Quantity",
        compute="_compute_orders_qty",
        help="Number of Sales associated in the grouped Sale Production",
    )

    order_ids = fields.One2many(
        string="Sales Orders",
        comodel_name="sale.order",
        inverse_name="mrp_sale_grouped_id",
    )

    # Quick access to MRP Production Orders
    mrp_production_ids = fields.One2many(
        comodel_name="mrp.production", compute="_compute_mrp_production_ids"
    )

    mrp_production_qty = fields.Integer(
        compute="_compute_production_qty",
    )

    # Quick access to Products withour any BoM
    product_wo_bom_ids = fields.One2many(
        comodel_name="product.product", compute="_compute_product_wo_bom_ids"
    )

    product_wo_bom_qty = fields.Integer(
        compute="_compute_product_wo_bom_qty",
    )

    # Default methods
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.depends("order_ids")
    def _compute_sales_state(self):
        for mrp_sale_grouped in self:
            if any(
                order.state in ["draft", "sent"]
                for order in mrp_sale_grouped.mapped("order_ids")
            ):
                mrp_sale_grouped.sales_state = "sales_in_progress"
            else:
                mrp_sale_grouped.sales_state = "all_sales_confirmed"

    @api.depends("mrp_production_ids")
    def _compute_production_state(self):
        for mrp_sale_grouped in self:
            if any(
                prods.state not in ["done", "cancel"]
                for prods in mrp_sale_grouped.mapped("mrp_production_ids")
            ):
                mrp_sale_grouped.production_state = "prod_in_progress"
            else:
                mrp_sale_grouped.production_state = "all_production_done"

    @api.depends("order_ids")
    def _compute_orders_qty(self):
        for mrp_sale_grouped in self:
            mrp_sale_grouped.orders_qty = len(mrp_sale_grouped.order_ids)

    # MRP Production
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

    # Products without any BoM
    @api.depends("order_ids")
    def _compute_product_wo_bom_ids(self):
        for grouped_prod in self.filtered(lambda x: x.order_ids):
            grouped_prod.product_wo_bom_ids = grouped_prod.mapped(
                "order_ids.order_line.product_id"
            ).filtered(lambda r: r.bom_count == 0)

    @api.depends("product_wo_bom_ids")
    def _compute_product_wo_bom_qty(self):
        for grouped_prod in self:
            grouped_prod.product_wo_bom_qty = len(grouped_prod.product_wo_bom_ids)

    @api.multi
    def confirm_all_sale_order(self):
        for sale_grouped in self:
            sale_grouped.mapped("order_ids").action_confirm()

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
