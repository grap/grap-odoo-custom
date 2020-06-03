# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PortalMixin(models.AbstractModel):
    _inherit = "portal.mixin"

    @api.multi
    def get_access_action(self, access_uid=None):
        return super(PortalMixin, self.with_context(
            force_website=False)).get_access_action(access_uid)
