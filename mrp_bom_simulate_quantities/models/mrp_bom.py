# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import csv
from io import StringIO

from odoo import _, api, fields, models
from odoo.exceptions import UserError


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
        string="Limiting product between Product 1 and 2",
        compute="_compute_bom_simulate_bom_lines_and_qty",
        store=True,
    )

    bom_simulate_product_2 = fields.Many2one(
        comodel_name="product.product",
        string="Second product to Simulate",
        domain="['&', ('id', 'in', product_ids_in_bom), \
                ('id', '!=', bom_simulate_product)]",
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
        store=True,
    )

    bom_simulate_bom_lines = fields.One2many(
        comodel_name="mrp.bom.line.simulate",
        inverse_name="bom_id",
        string="Simulated BoM Lines",
        compute="_compute_bom_simulate_bom_lines_and_qty",
        store=True,
    )

    product_ids_in_bom = fields.Many2many(
        comodel_name="product.product",
        string="Technical field to compute bom_simulate_product domain",
        compute="_compute_product_ids_in_bom",
    )

    @api.onchange("bom_line_ids")
    def _onchange_bom_simulate_product(self):
        # Select main and secondary product
        for bom in self.filtered(lambda b: b.bom_line_ids):
            sorted_lines = sorted(
                bom.bom_line_ids,
                key=lambda line: line.product_qty / line.product_uom_id.ratio
                if line.product_uom_id.ratio
                else 0,
                reverse=True,
            )

            bom.bom_simulate_product = (
                sorted_lines[0].product_id.id
                if sorted_lines and sorted_lines[0].product_id
                else False
            )

            bom.bom_simulate_product_2 = (
                sorted_lines[1].product_id.id
                if len(sorted_lines) > 1 and sorted_lines[1].product_id
                else False
            )

    def toggle_show_second_product(self):
        for bom in self:
            bom.show_second_product = not bom.show_second_product

    # Compute functions
    @api.depends("bom_line_ids")
    def _compute_product_ids_in_bom(self):
        for bom in self:
            bom.product_ids_in_bom = bom.bom_line_ids.mapped("product_id")

    def _get_bom_line_qty(self, product, default_qty=1.0):
        product_line = next(
            (line for line in self.bom_line_ids if line.product_id == product),
            None,
        )
        return product_line.product_qty if product_line else default_qty

    # Computed fields
    @api.depends(
        "bom_simulate_product",
        "bom_simulate_product_qty",
        "bom_simulate_product_2",
        "bom_simulate_product_qty_2",
        "show_second_product",
        "bom_line_ids",
        "product_qty",
    )
    def _compute_bom_simulate_bom_lines_and_qty(self):
        DEFAULT_ROUND = 2
        DEFAULT_QTY = 1.0

        for bom in self:
            simulate_prod = bom.bom_simulate_product
            product_qty_in_bom = bom._get_bom_line_qty(simulate_prod, DEFAULT_QTY)

            if bom.show_second_product and bom.bom_simulate_product_2:
                simulate_prod_2 = bom.bom_simulate_product_2
                simulate_prod_qty_2 = bom.bom_simulate_product_qty_2
                product_qty_in_bom_2 = bom._get_bom_line_qty(
                    simulate_prod_2, DEFAULT_QTY
                )

                # Compare ratio between the two products in BoM and in simulation
                # in ordre to find which is limiting product
                bom_products_division = (
                    product_qty_in_bom / product_qty_in_bom_2
                    if product_qty_in_bom_2
                    else 0
                )
                bom_simulate_products_division = (
                    bom.bom_simulate_product_qty / simulate_prod_qty_2
                    if simulate_prod_qty_2
                    else 0
                )
                # Then set simulate qty and choosen product
                if bom_simulate_products_division > bom_products_division:
                    bom.limiting_product = simulate_prod_2
                    simulate_qty = simulate_prod_qty_2 or DEFAULT_QTY
                    # Choose BoM Line Product 2 quantity
                    product_qty_in_bom = product_qty_in_bom_2
                else:
                    bom.limiting_product = bom.bom_simulate_product
                    simulate_qty = bom.bom_simulate_product_qty or DEFAULT_QTY
            else:
                simulate_qty = bom.bom_simulate_product_qty or DEFAULT_QTY
                bom.limiting_product = False

            # Calculate ratio with choosen product
            ratio = (
                simulate_qty / product_qty_in_bom if product_qty_in_bom else DEFAULT_QTY
            )

            # Change simulating lines with ratio
            bom.bom_simulate_bom_lines = [(5, 0, 0)] + [
                (
                    0,
                    0,
                    {
                        "bom_id": bom.id,
                        "product_id": line.product_id.id,
                        "product_qty": round(line.product_qty * ratio, DEFAULT_ROUND),
                        "product_uom_id": line.product_uom_id.id,
                    },
                )
                for line in bom.bom_line_ids
            ]

            bom.bom_simulate_bom_qty = round(bom.product_qty * ratio, DEFAULT_ROUND)

    @api.depends("bom_simulate_product", "bom_simulate_product_2")
    def _compute_bom_simulate_product_uom(self):
        for bom in self:
            bom.bom_simulate_product_uom = bom.bom_simulate_product.uom_id
            bom.bom_simulate_product_uom_2 = bom.bom_simulate_product_2.uom_id

    def action_export_simulation_csv(self):
        self.ensure_one()

        if not self.bom_simulate_bom_lines:
            raise UserError(_("No simulated lines to export."))

        # Create CSV content
        output = StringIO()
        writer = csv.writer(
            output, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(
            [
                _("Product"),
                _("Quantity"),
                _("Unit of Measure"),
            ]
        )

        for line in self.bom_simulate_bom_lines:
            writer.writerow(
                [
                    line.product_id.display_name,
                    line.product_qty,
                    line.product_uom_id.name,
                ]
            )

        csv_content = output.getvalue()
        output.close()

        # Create attachment
        filename = f"simulation_{self.product_tmpl_id.display_name}_\
                {self.bom_simulate_bom_qty}.csv"
        attachment = self.env["ir.attachment"].create(
            {
                "name": filename,
                "type": "binary",
                "datas": base64.b64encode(csv_content.encode()),
                "res_model": self._name,
                "res_id": self.id,
                "mimetype": "text/csv",
            }
        )

        # Return URL to download
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "new",
        }
