# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models

from odoo.addons import decimal_precision as dp


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    currency_id = fields.Many2one(related="product_tmpl_id.currency_id")
    # Fields related to cost
    product_standard_price = fields.Float(compute="_compute_product_standard_price")
    standard_price_total = fields.Float(
        string="BoM Cost",
        track_visibility="onchange",
        digits=dp.get_precision("Product Price"),
        compute="_compute_standard_price_total",
    )
    diff_product_bom_standard_price = fields.Float(
        digits=dp.get_precision("Product Price"),
        compute="_compute_diff_product_bom_standard_price",
    )

    # Fields related to sale price
    product_sale_price = fields.Float(
        string="Product Sale Price", related="product_id.lst_price"
    )
    product_margin_rate = fields.Float(related="product_id.standard_margin_rate")
    product_margin_rate_percentage = fields.Float(
        string="Product Margin", compute="_compute_product_margin_rate_percentage"
    )

    #
    # Other functions
    #
    @api.multi
    @api.depends("product_id", "product_id.standard_price")
    def _compute_product_standard_price(self):
        for bom in self:
            bom.product_standard_price = bom.product_id.standard_price

    @api.multi
    @api.depends("product_id", "bom_line_ids")
    def _compute_standard_price_total(self):
        for bom in self:
            bom.standard_price_total = sum(
                x.standard_price_subtotal for x in bom.bom_line_ids
            )

    @api.multi
    @api.depends("product_id.standard_price", "standard_price_total")
    def _compute_diff_product_bom_standard_price(self):
        for bom in self.filtered(lambda x: x.product_id):
            bom.diff_product_bom_standard_price = (
                bom.product_id.standard_price - bom.standard_price_total
            )

    @api.multi
    @api.depends("product_margin_rate")
    def _compute_product_margin_rate_percentage(self):
        for bom in self:
            bom.product_margin_rate_percentage = bom.product_margin_rate / 100

    # Functions to change product fields
    @api.multi
    def set_product_standard_price(self):
        for bom in self.filtered(lambda x: x.product_id):
            old_product_standard_price = bom.product_id.standard_price
            bom.product_id.standard_price = bom.standard_price_total
            diff_percentage = (
                (bom.product_id.standard_price - old_product_standard_price)
                / old_product_standard_price
                * 100
                if old_product_standard_price != 0
                else 100
            )
            diff_percentage_str = str(round(diff_percentage, 1)) + "%"
            self.env.user.notify_success(
                message=(_("Price difference : %s") % (diff_percentage_str,)),
                title=(_("New standard price for %s") % bom.product_id.name),
            )
