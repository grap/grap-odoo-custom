# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # ========== Fields related to weight
    bom_components_total_net_weight = fields.Float(
        string="Net weight of components",
        compute="_compute_bom_components_total_net_weight",
    )
    bom_components_total_gross_weight = fields.Float(
        string="Gross weight of components",
        compute="_compute_bom_components_total_gross_weight",
    )
    diff_bom_qty_and_net_quantities = fields.Float(
        digits=dp.get_precision("Product Price"),
        compute="_compute_diff_bom_qty_and_net_quantities",
    )
    display_set_quantity_with_net_quantities = fields.Boolean(
        default=True,
        compute="_compute_display_set_quantity_with_net_quantities",
    )

    @api.depends("bom_line_ids.line_net_weight")
    def _compute_bom_components_total_net_weight(self):
        for bom in self:
            bom.bom_components_total_net_weight = sum(
                bom.bom_line_ids.mapped("line_net_weight")
            )

    @api.depends("bom_line_ids.line_gross_weight")
    def _compute_bom_components_total_gross_weight(self):
        for bom in self:
            bom.bom_components_total_gross_weight = sum(
                bom.bom_line_ids.mapped("line_gross_weight")
            )

    @api.multi
    @api.depends("product_qty", "bom_components_total_net_weight")
    def _compute_diff_bom_qty_and_net_quantities(self):
        for bom in self:
            _diff_bom_qty_and_net_quantities = round(
                (bom.product_qty - bom.bom_components_total_net_weight), 2
            )
            bom.diff_bom_qty_and_net_quantities = _diff_bom_qty_and_net_quantities

    @api.multi
    @api.depends("product_tmpl_id.uom_id")
    def _compute_display_set_quantity_with_net_quantities(self):
        for bom in self.filtered(lambda x: x.product_tmpl_id):
            bom.display_set_quantity_with_net_quantities = (
                True if bom.product_tmpl_id.uom_id.measure_type == "weight" else False
            )

    @api.multi
    def set_bom_quantity_with_net_quantities(self):
        for bom in self:
            bom.product_qty = bom.bom_components_total_net_weight
