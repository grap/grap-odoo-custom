# Copyright (C) 2021-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class WizardPosMoveReason(models.TransientModel):
    _inherit = 'wizard.pos.move.reason'

    @api.multi
    def _prepare_statement_line(self):
        res = super()._prepare_statement_line()
        if self.session_id.stop_at:
            res["date"] = self.session_id.stop_at
        return res
