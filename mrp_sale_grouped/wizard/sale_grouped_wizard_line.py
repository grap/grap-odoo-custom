# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleGroupedWizardLine(models.TransientModel):
    _name = "sale.grouped.wizard.line"
    _description = (
        "Wizard line for printing purchase list from selected bill of materials"
    )

    # Columns Section
    wizard_id = fields.Many2one(comodel_name="sale.grouped.wizard")

    sale_id = fields.Many2one(comodel_name="sale.order", string="Sale order")
    #
    # currency_id = fields.Many2one(
    #     comodel_name="res.currency",
    #     related="bom_id.currency_id",
    # )
    #
    # bom_description = fields.Char(
    #     string="Description", compute="_compute_bom_description"
    # )
    #
    # bom_product_qty = fields.Float(string="BoM Qty", related="bom_id.product_qty")
    #
    # bom_uom_id = fields.Many2one(
    #     related="bom_id.product_uom_id",
    #     string="UoM",
    # )
    #
    # quantity = fields.Float(
    #     string="Desired Quantity",
    #     default=1,
    # )
    #
    # wizard_line_subtotal = fields.Float(
    #     string="Cost",
    #     digits=dp.get_precision("Product Price"),
    # )
    #
    # @api.depends("bom_id")
    # def _compute_bom_description(self):
    #     for line in self.filtered(lambda x: x.bom_id):
    #         line.bom_description = line.bom_id.description_short
    #
    # @api.onchange("bom_id", "quantity")
    # def _onchange_wizard_line_cost(self):
    #     bom_qty = 1 if self.bom_product_qty == 0 else self.bom_product_qty
    #     self.wizard_line_subtotal = (
    #         self.bom_id.standard_price_total * self.quantity / bom_qty
    #     )
