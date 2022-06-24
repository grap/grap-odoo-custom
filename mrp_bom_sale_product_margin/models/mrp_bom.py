# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # TODO : warning dans les modules de base, pas forcement de product_id

    currency_id = fields.Many2one(related="product_tmpl_id.currency_id")
    # Fields related to cost
    standard_price_total = fields.Float(
        string="BoM Cost",
        track_visibility='onchange',
        digits=dp.get_precision('Product Price'),
        compute="_compute_standard_price_total"
    )
    diff_product_bom_standard_price = fields.Float(
        digits=dp.get_precision('Product Price'),
        compute="_diff_product_bom_standard_price")
    # Idea : text pour dire que le prix est ok avec l'article où que non, il est actuellement à tant ?
    # surement trop lourd pour rien
    # text_diff_product_bom_standard_price = fields.Char()

    # Fields related to sale price
    bom_margin_state = fields.Selection(related="product_id.margin_state")
    bom_theoretical_price = fields.Float(related="product_id.theoretical_price")
    bom_lst_price = fields.Float(
        compute="_compute_lst_price",
        inverse="_inverse_lst_price",
        store=True)
    bom_standard_margin_rate = fields.Float(related="product_id.standard_margin_rate")

    #
    # Other functions
    #
    @api.multi
    @api.depends("product_id")
    def _compute_lst_price(self):
        for bom in self.filtered(lambda x: x.product_id):
            bom.bom_lst_price = bom.product_id.lst_price

    @api.depends("lst_price")
    def _inverse_lst_price(self):
        for bom in self.filtered(lambda x: x.product_id):
            bom.product_id.lst_price = bom.bom_lst_price

    @api.multi
    @api.depends("product_id", "bom_line_ids")
    def _compute_standard_price_total(self):
        for bom in self:
            bom.standard_price_total = sum(
                x.standard_price_subtotal for x in bom.bom_line_ids
            )

    @api.multi
    @api.depends("product_id.standard_price", "standard_price_total")
    def _diff_product_bom_standard_price(self):
        for bom in self.filtered(lambda x: x.product_id):
            bom.diff_product_bom_standard_price =\
                bom.product_id.standard_price - bom.standard_price_total
            print("======== DIFF =" + str(bom.diff_product_bom_standard_price))

    # Custom Section
    @api.multi
    def use_theoretical_price(self):
        for bom in self:
            bom.bom_lst_price = bom.theoretical_price

    # Functions to change product fields
    @api.multi
    def set_product_standard_price(self):
        for bom in self.filtered(lambda x: x.product_id):
            old_product_standard_price = bom.product_id.standard_price
            bom.product_id.standard_price = bom.standard_price_total
            self.env.user.notify_success(
                message=_("Cost price is set to $%s (old price was $%s)" %
                          (
                              round(bom.product_id.standard_price, 2),
                              round(old_product_standard_price, 2)
                          )
                          ),
                title=_("New Standard Price for %s" % bom.product_id.name),
            )
