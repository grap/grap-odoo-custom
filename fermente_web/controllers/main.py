# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import functools

from odoo import http
from odoo.modules import get_resource_path

from odoo.addons.web import controllers


class Binary(controllers.binary.Binary):
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
        dbname = dbname or http.request.session.db or ""

        placeholder = functools.partial(
            get_resource_path, "fermente_web", "static", "src", "img"
        )
        file_name = "undefined_database"
        for name in ["grap", "caap", "mache", "fermente"]:
            if dbname.startswith(f"{name}_production"):
                file_name = name

        return http.Stream.from_path(placeholder(f"{file_name}.png")).get_response()
