# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import pytz
from datetime import datetime

from openerp import api, models, tools


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.multi
    def _prepare_date_sale_move_point_of_sale(self):
        context_tz = pytz.timezone(self.env.user.tz)
        timestamp = datetime.strptime(
            self.date_order, tools.DEFAULT_SERVER_DATETIME_FORMAT)
        utc_timestamp = pytz.utc.localize(timestamp, is_dst=False)
        tz_timestamp = utc_timestamp.astimezone(context_tz)
        return tz_timestamp.strftime("%Y-%m-%d")
