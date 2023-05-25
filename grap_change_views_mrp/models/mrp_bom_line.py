# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    def go_to_bom(self):
        result = super().go_to_bom()
        if self.product_id.bom_count == 1:
            form_view = self.env.ref("grap_change_views_mrp.view_mrp_bom_form_grap")
            result["views"] = [(form_view.id, "form")]
        return result
