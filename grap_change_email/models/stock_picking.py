# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_picking_send(self):
        res = super().action_picking_send()
        template = self.env.ref("grap_change_email.email_template_stock_picking")
        res["context"].update(
            {
                "default_use_template": bool(template.id),
                "default_template_id": template.id,
            }
        )
        return res
