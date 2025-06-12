# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # First Product
    bom_simulate_product = fields.Many2one(
        comodel_name="product.product",
        string="Product to Simulate",
        domain="[('id', 'in', product_ids_in_bom)]",
    )

    bom_simulate_product_uom = fields.Many2one(
        comodel_name="uom.uom", compute="_compute_bom_simulate_product_uom"
    )

    bom_simulate_product_qty = fields.Float(
        string="Quantity to Simulate",
        default=0,
    )

    # Second Product
    show_second_product = fields.Boolean()

    limiting_product = fields.Many2one(
        comodel_name="product.product",
        string="Limiting similating product betweend Product 1 and 2",
    )

    bom_simulate_product_2 = fields.Many2one(
        comodel_name="product.product",
        string="Second product to Simulate",
        domain="[('id', 'in', product_ids_in_bom)]",
    )

    bom_simulate_product_uom_2 = fields.Many2one(
        comodel_name="uom.uom", compute="_compute_bom_simulate_product_uom"
    )

    bom_simulate_product_qty_2 = fields.Float(
        string="Quantity Product 2 to Simulate",
        default=0,
    )

    # Others fields
    bom_simulate_bom_qty = fields.Float(
        string="BoM quantity simulated",
        compute="_compute_bom_simulate_bom_lines_and_qty",
    )

    bom_simulate_bom_lines = fields.One2many(
        comodel_name="mrp.bom.line.simulate",
        inverse_name="bom_id",
        string="Simulated BoM Lines",
        compute="_compute_bom_simulate_bom_lines_and_qty",
    )

    product_ids_in_bom = fields.Many2many(
        comodel_name="product.product",
        compute="_compute_product_ids_in_bom",
        string="Technical field to compute bom_simulate_product domain",
    )

    # Functions
    @api.onchange("bom_line_ids")
    def _onchange_bom_simulate_product(self):
        for bom in self.filtered(lambda b: b.bom_line_ids):
            max_line = max(bom.bom_line_ids, key=lambda x: x.product_qty or 0)
            bom.bom_simulate_product = (
                max_line.product_id.id if max_line.product_id else False
            )

    def toggle_show_second_product(self):
        for bom in self:
            bom.show_second_product = not bom.show_second_product
            # Reinit second product
            bom.bom_simulate_product_2 = False
            bom.bom_simulate_product_qty_2 = 0

    # Compute functions
    @api.depends("bom_line_ids")
    def _compute_product_ids_in_bom(self):
        for bom in self:
            bom.product_ids_in_bom = bom.bom_line_ids.mapped("product_id")

    # Computed fields
    @api.depends(
        "bom_simulate_product",
        "bom_simulate_product_qty",
        "bom_simulate_product_qty_2",
        "bom_line_ids",
        "product_qty",
    )
    def _compute_bom_simulate_bom_lines_and_qty(self):
        for bom in self:
            # Get product quantity in BoM Lines
            product_line = bom.bom_line_ids.filtered(
                lambda l: l.product_id == bom.bom_simulate_product
            )
            product_qty_in_bom = product_line[0].product_qty if product_line else 1.0

            product_line_2 = bom.bom_line_ids.filtered(
                lambda l: l.product_id == bom.bom_simulate_product_2
            )
            product_qty_in_bom_2 = (
                product_line_2[0].product_qty if product_line_2 else 1.0
            )

            # Find which is limiting product and set simulate quantity
            bom_products_division = (
                product_qty_in_bom / product_qty_in_bom_2 if product_qty_in_bom_2 else 0
            )
            bom_simulation_products_division = (
                bom.bom_simulate_product_qty / bom.bom_simulate_product_qty_2
                if bom.bom_simulate_product_qty_2
                else 0
            )
            if bom_simulation_products_division > bom_products_division:
                limiting_product = bom.bom_simulate_product_2
                simulate_qty = bom.bom_simulate_product_qty_2 or 1.0
            else:
                limiting_product = bom.bom_simulate_product
                simulate_qty = bom.bom_simulate_product_qty or 1.0

            # Calculate ratio
            ratio = simulate_qty / product_qty_in_bom if product_qty_in_bom else 1.0

            # Change simulating lines with ratio
            lines = []
            for line in bom.bom_line_ids:
                lines.append(
                    (
                        0,
                        0,
                        {
                            "bom_id": bom.id,
                            "product_id": line.product_id.id,
                            "product_qty": line.product_qty * ratio,
                            "product_uom_id": line.product_uom_id.id,
                        },
                    )
                )

            bom.bom_simulate_bom_lines = lines
            bom.bom_simulate_bom_qty = bom.product_qty * ratio
            bom.limiting_product = limiting_product

    @api.depends("bom_simulate_product", "bom_simulate_product_2")
    def _compute_bom_simulate_product_uom(self):
        for bom in self:
            bom.bom_simulate_product_uom = bom.bom_simulate_product.uom_id
            bom.bom_simulate_product_uom_2 = bom.bom_simulate_product_2.uom_id
