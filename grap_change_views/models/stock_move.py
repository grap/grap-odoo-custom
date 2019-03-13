# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Column Section
    workflow_description = fields.Char(
        compute='_compute_workflow_description', string='Workflow',
        store=True)

    # compute Section
    @api.multi
    @api.depends('location_id', 'location_dest_id')
    def _compute_workflow_description(self):
        for move in self:
            move.workflow_description = '%s >> %s' % (
                move.location_id.name, move.location_dest_id.name)
