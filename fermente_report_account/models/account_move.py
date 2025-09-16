# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models

from odoo.addons.http_routing.models.ir_http import slugify


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = "account.move"

    def _get_report_base_filename(self):
        self.ensure_one()
        return _("Invoice__{number}__{partner}__{date}").format(
            number=slugify(self.name or "")
            or (self.state == "draft" and _("Draft"))
            or "",
            partner=self.partner_id and slugify(self.partner_id.name) or _("Anonymous"),
            date=self.invoice_date and slugify(str(self.invoice_date)) or "",
        )
