# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    _order = 'create_date desc'

    state = fields.Selection(
        related='order_id.state', string='State', readonly=True)

    partner_id = fields.Many2one(
        related='order_id.partner_id', comodel_name='res.partner',
        string='Customer', readonly=True)
