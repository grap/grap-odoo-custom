# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # New fields
    has_bom = fields.Boolean(
        compute="_compute_has_bom",
        help="Click to access BoM of this product.",
        default=False,
    )

    @api.multi
    @api.depends("product_id", "product_id.bom_count")
    def _compute_has_bom(self):
        for bom_line in self:
            bom_line.has_bom = bom_line.product_id.bom_count

    def go_to_bom(self):
        self.ensure_one()
        result = self.env.ref("mrp.mrp_bom_form_action").read()[0]
        # Go to only BoM
        if self.product_id.bom_count == 1:
            form_view = self.env.ref("mrp.mrp_bom_form_view")
            result["views"] = [(form_view.id, "form")]
            result["res_id"] = self.product_id.bom_ids[0].id
            result["context"] = {
                "form_view_initial_mode": "edit",
            }
        # Show different BoMs
        else:
            tree_view = self.env.ref("mrp.mrp_bom_tree_view")
            boms = self.product_id.mapped("bom_ids")
            result["views"] = [(tree_view.id, "tree")]
            result["domain"] = [("id", "in", boms.ids)]
        return result
