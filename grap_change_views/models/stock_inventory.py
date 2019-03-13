# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class StockInventory(models.Model):
    _inherit = 'stock.inventory'
    _order = 'date desc, name'

    # Action Section
    @api.multi
    def action_view_lines(self):
        self.ensure_one()
        action = self.env.ref(
            'grap_change_views.action_view_lines_tree')
        action_data = action.read()[0]
        action_data['domain'] = "[('id','in',[" +\
            ','.join(map(str, self.line_ids.ids)) + "])]"
        return action_data
