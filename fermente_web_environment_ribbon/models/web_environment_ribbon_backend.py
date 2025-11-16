# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class WebEnvironmentRibbonBackend(models.AbstractModel):
    _inherit = "web.environment.ribbon.backend"

    @api.model
    def _prepare_ribbon_format_vals(self):
        res = super()._prepare_ribbon_format_vals()
        splitted = res["db_name"].split("__")
        if len(splitted) == 3:
            name_part = splitted[0].replace("_production", "")
            date_part = splitted[1]
            date_part_splitted = date_part.split("_")
            if len(date_part_splitted) == 3:
                date_part = (
                    f"{date_part_splitted[2]}"
                    f"/{date_part_splitted[1]}/"
                    f"{date_part_splitted[0]}"
                )
            time_part = splitted[2]
            time_part_splitted = time_part.split("_")
            if len(time_part_splitted) == 3:
                time_part = f"{time_part_splitted[0]}:{time_part_splitted[1]}"

            res["db_name"] = f"{name_part}<br />{date_part} {time_part}"
        return res
