# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BomPrintWizardLine(models.TransientModel):
    _name = "bom.print.wizard.line"
    _description = "Wizard line for printing bill of materials"

    # Columns Section
    wizard_id = fields.Many2one(comodel_name="bom.print.wizard")

    bom_id = fields.Many2one(
        comodel_name="mrp.bom", string="Bill Of Material", required=True
    )

    bom_allergens_ids = fields.Many2many(
        comodel_name="product.allergen",
        related="bom_id.bom_allergen_ids",
        readonly=False,
    )

    quantity = fields.Integer(string="Quantity", required=True, default=1)
