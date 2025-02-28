# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import functools

from odoo import http
from odoo.http import db_monodb, request
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
        if request.session.db:
            dbname = request.session.db
        elif dbname is None:
            dbname = db_monodb()

        placeholder = functools.partial(
            get_resource_path, "grap_theme", "static", "src", "img"
        )
        if dbname.startswith("grap"):
            return http.send_file(placeholder("grap.png"))
        elif dbname.startswith("caap"):
            return http.send_file(placeholder("caap.png"))
        else:
            return http.send_file(placeholder("undefined_database.png"))
