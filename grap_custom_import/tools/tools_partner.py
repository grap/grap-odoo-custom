# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _


def _handle_partner_name(self, vals):
    """
    - Sanitize the partner name
    - search if partner still exist and raise an error if yes
    """
    ResPartner = self.env["res.partner"]
    res = vals.copy()
    name = res.get("name", False)
    # TODO don't hardcode '*'
    # get the value from the ir.config.parameter.
    name = name.replace("*", "")
    name = name.strip()
    partners = ResPartner.search([("name", "=", name)])
    if partners:
        raise Exception(
            _("The following item(s) still exist %s")
            % ",".join(partners.mapped("name"))
        )
    res["name"] = name
    return res
