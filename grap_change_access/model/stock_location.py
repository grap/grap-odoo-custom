# -*- coding: utf-8 -*-
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    @api.multi
    def name_get(self):
        res = super(StockLocation, self).name_get()
        return res

#    def _complete_name(self, cr, uid, ids, name, args, context=None):
#        """ Forms complete name of location from parent location to child
#        location.
#        @return: Dictionary of values
#        """
#        res = {}
#        print ">>>>>>>>>>>>>>>>>>>>>>>>> grap_change_access"
#        print "_complete_name"
#        for m in self.browse(cr, uid, ids, context=context):
#            names = [m.name]
#            parent = m.location_id
#            while parent:
#                try:
#                    names.append(parent.name)
#                    parent = parent.location_id
#                except:
#                    parent = None
#            res[m.id] = ' / '.join(reversed(names))
#        return res
