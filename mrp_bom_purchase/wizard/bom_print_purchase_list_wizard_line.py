# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BomPrintPurchaseListWizardLine(models.TransientModel):
    _name = "bom.print.purchase.list.wizard.line"
    _description = (
        "Wizard line for printing purchase list from selected bill of materials"
    )

    # Columns Section
    wizard_id = fields.Many2one(comodel_name="bom.print.purchase.list.wizard")

    bom_id = fields.Many2one(comodel_name="mrp.bom", string="Bill Of Material")

    bom_qty = fields.Float(sting="Desired Quantity", default=1)
