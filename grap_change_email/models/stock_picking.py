# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_picking_send(self):
        res = super().action_picking_send()
        picking_obj = self.env["stock.picking"]
        picking_id = res["context"]["default_res_id"]
        picking = picking_obj.search([("id", "=", picking_id)])

        if picking.picking_type_id.default_location_dest_id.usage == "internal":
            template = self.env.ref("grap_change_email.email_template_stock_picking_in")
        else:
            template = self.env.ref(
                "grap_change_email.email_template_stock_picking_out"
            )

        res["context"].update(
            {
                "default_use_template": bool(template.id),
                "default_template_id": template.id,
            }
        )
        return res
