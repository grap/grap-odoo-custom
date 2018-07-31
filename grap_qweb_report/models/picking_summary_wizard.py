# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class PickingSummaryWizard(models.TransientModel):
    _name = 'picking.summary.wizard'

    # Default Section
    def _default_picking_line_qty(self):
        return len(self._context.get('active_ids', []))

    def _default_picking_line_ids(self):
        picking_obj = self.env['stock.picking']
        res = []
        picking_ids = self._context.get('active_ids', [])
        for picking in picking_obj.browse(picking_ids):
            res.append((0, 0, {
                'picking_id': picking.id,
            }))
        return res

    def _default_product_line_ids(self):
        picking_obj = self.env['stock.picking']
        res = []
        product_lines = {}
        picking_ids = self._context.get('active_ids', [])
        for picking in picking_obj.browse(picking_ids):
            for move in picking.move_lines:
                # TODO FIXME, manage different uom by stock.move
                if move.product_id.id not in product_lines.keys():
                    product_lines[move.product_id.id] = move.product_qty
                else:
                    product_lines[move.product_id.id] += move.product_qty

        for product_id, quantity_total in product_lines.iteritems():
            res.append((0, 0, {
                'product_id': product_id,
                'quantity_total': quantity_total,
            }))
        return res

    # Columns Section
    print_summary = fields.Boolean(string='Print Summary', default=True)

    print_detail = fields.Boolean(string='Print Detail', default=True)

    product_line_ids = fields.One2many(
        comodel_name='picking.summary.wizard.product',
        inverse_name='wizard_id', default=_default_product_line_ids)

    standard_price_total = fields.Float(
        compute='_compute_standard_price_total')

    picking_line_ids = fields.One2many(
        comodel_name='picking.summary.wizard.picking',
        inverse_name='wizard_id', default=_default_picking_line_ids)

    picking_line_qty = fields.Integer(
        string='Delivery Qty', readonly=True,
        default=_default_picking_line_qty)

    # Compute Section
    @api.multi
    def _compute_standard_price_total(self):
        self.ensure_one()
        self.standard_price_total = sum(
            self.mapped('product_line_ids.standard_price_total'))
