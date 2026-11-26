# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
from datetime import datetime

from odoo import api, models


class WebEnvironmentRibbonBackend(models.AbstractModel):
    _inherit = "web.environment.ribbon.backend"

    @api.model
    def _prepare_ribbon_format_vals(self):
        res = super()._prepare_ribbon_format_vals()
        regex = re.compile(
            r"(?P<company_name>.*)_production.*(?P<year>\d{4})_(?P<month>\d{2})_(?P<day>\d{2})__(?P<hour>\d{2})_(?P<minute>\d{2})_\d{2}"
        )
        db_name = res["db_name"]
        re_match = regex.match(db_name)

        if re_match:
            db_date = datetime(
                int(re_match.group("year")),
                int(re_match.group("month")),
                int(re_match.group("day")),
                int(re_match.group("hour")),
                int(re_match.group("minute")),
            )
            extra_char = ""
            if (datetime.now() - db_date).days > 0:
                extra_char = " &#x26A0; "

            res["db_name"] = (
                f"{re_match.group('company_name')}"
                "<br />"
                f"{extra_char}"
                f"{db_date.strftime('%d/%m/%Y %Hh%M')}"
                f"{extra_char}"
            )

        return res
