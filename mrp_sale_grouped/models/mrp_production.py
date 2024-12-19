# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def open_mo(self):
        self.ensure_one()
        result = self.env['ir.actions.act_window']._for_xml_id('mrp.action_mrp_production_form')
        form_view = self.env.ref("mrp.mrp_production_form_view")
        result["views"] = [(form_view.id, "form")]
        result["res_id"] = self.id
        result["context"] = {
            "form_view_initial_mode": "edit",
        }
        return result
