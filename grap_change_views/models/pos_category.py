# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields


class PosCategory(models.Model):
    _inherit = 'pos.category'
    _order = 'complete_name_order'

    # Columns Section
    complete_name_order = fields.Char(
        string='Complete Name Stored', store=True,
        compute='_compute_complete_name_order')

    product_ids = fields.One2many(
        comodel_name='product.product', inverse_name='pos_categ_id',
        string='Products', readonly=True)

    product_qty = fields.Integer(
        string='Product Qty', compute='_compute_product_qty', store=True)

    # Compute Section
    @api.depends('name', 'parent_id.name')
    def _compute_complete_name_order(self):
        for category in self:
            category.complete_name_order = category.complete_name

    @api.depends('product_ids')
    def _compute_product_qty(self):
        for category in self:
            category.product_qty = len(category.product_ids)
