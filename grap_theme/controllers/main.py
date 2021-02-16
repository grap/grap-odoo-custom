# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import functools

from odoo import http
from odoo.modules import get_resource_path

from odoo.addons.web import controllers


class Binary(controllers.main.Binary):
    @http.route(
        [
            "/web/binary/company_logo",
            "/logo",
            "/logo.png",
        ],
        type="http",
        auth="none",
        cors="*",
    )
    def company_logo(self, dbname=None, **kw):
        placeholder = functools.partial(
            get_resource_path, "grap_theme", "static", "src", "img"
        )
        return http.send_file(placeholder("grap_logo.png"))
