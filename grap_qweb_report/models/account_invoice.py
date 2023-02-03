# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from slugify import slugify

from odoo import _, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice", "report.custom.message.mixin"]

    def _get_report_base_filename(self):
        self.ensure_one()
        return _("Invoice__{number}__{partner}__{date}").format(
            number=slugify(self.number, lowercase=False)
            or (self.state == "draft" and _("Draft"))
            or "",
            partner=self.partner_id and slugify(self.partner_id.name) or _("Anonymous"),
            date=self.date_invoice and slugify(str(self.date_invoice)) or "",
        )
