# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    currency_id = fields.Many2one(related="product_tmpl_id.currency_id")

    def action_mrp_bom_wizard_production(self):
        return {
            "name": _("Production wizard"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "bom.wizard.production",
            "views": [
                [
                    self.env.ref(
                        "mrp_bom_wizard_production.view_bom_wizard_production_form"
                    ).id,
                    "form",
                ]
            ],
            "target": "new",
        }
