# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    bom_components_total_net_weight = fields.Float(
        string="Net weight of components",
        help="Net weight of components in kg",
        compute="_compute_bom_components_total_net_weight",
    )
    bom_components_total_gross_weight = fields.Float(
        string="Gross weight of components",
        help="Gross weight of components in kg",
        compute="_compute_bom_components_total_gross_weight",
    )
    display_set_quantity_with_net_quantities = fields.Boolean(
        compute="_compute_display_set_quantity_with_net_quantities",
        help="Technical field used to display or hide button "
        "set_bom_quantity_with_net_quantities in the BoM Form view",
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

    @api.depends(
        "product_qty",
        "product_uom_id",
        "bom_components_total_net_weight",
        "product_tmpl_id.uom_id",
    )
    def _compute_display_set_quantity_with_net_quantities(self):
        for bom in self:
            # Calculate weight difference between product weight and its components
            diff_bom_qty_and_net_quantities = round(
                bom.product_qty * bom.product_uom_id.factor_inv
                - bom.bom_components_total_net_weight,
                2,
            )
            # .. and display button only for weightable products
            bom.display_set_quantity_with_net_quantities = (
                diff_bom_qty_and_net_quantities != 0
                and bom.product_tmpl_id.uom_id.measure_type == "weight"
            )

    def set_bom_quantity_with_net_quantities(self):
        for bom in self:
            bom.product_qty = (
                bom.bom_components_total_net_weight * bom.product_uom_id.factor
            )
