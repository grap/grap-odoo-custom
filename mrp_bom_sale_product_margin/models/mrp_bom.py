# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models

from odoo.addons import decimal_precision as dp


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    currency_id = fields.Many2one(related="product_tmpl_id.currency_id")
    # Fields related to cost
    product_standard_price = fields.Float(related="product_id.standard_price")
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
    product_sale_price = fields.Float(related="product_id.lst_price")
    product_margin_rate = fields.Float(related="product_id.standard_margin_rate")

    #
    # Other functions
    #
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

    # Functions to change product fields
    @api.multi
    def set_product_standard_price(self):
        for bom in self.filtered(lambda x: x.product_id):
            old_product_standard_price = bom.product_id.standard_price
            bom.product_id.standard_price = bom.standard_price_total
            self.env.user.notify_success(
                message=_(
                    "Cost price is set to $%s (former price was $%s)"
                    % (
                        round(bom.product_id.standard_price, 2),
                        round(old_product_standard_price, 2),
                    )
                ),
                title=_("New standard price for %s" % bom.product_id.name),
            )
