# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class WebEnvironmentRibbonBackend(models.AbstractModel):
    _inherit = "web.environment.ribbon.backend"

    @api.model
    def _prepare_ribbon_format_vals(self):
        return {
            "db_name": "<br />".join(
                self.env.cr.dbname.replace("_production__", "___").split("___")
            )
        }
