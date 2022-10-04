# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BomPrintPurchaseListWizardLine(models.TransientModel):
    _name = "bom.print.purchase.list.wizard.line"
    _description = (
        "Wizard line for printing purchase list from selected bill of materials"
    )

    # Columns Section
    wizard_id = fields.Many2one(comodel_name="bom.print.purchase.list.wizard")

    bom_id = fields.Many2one(comodel_name="mrp.bom", string="Bill Of Material")

    bom_product_qty = fields.Float(string="Bom made for this quantity",)

    bom_qty = fields.Float(string="Desired Quantity",)

    bom_uom_id = fields.Many2one(comodel_name="uom.uom", string="Bom uom",)
    # TODO : soucis avec le product_uom_id qui est forcement 1PCE, donc naze. C'est nativement ça mais modifiable. Voir à qu'il soit lié au product. VOir pourquoi c'est commenté dans grap_change_views_mrp et faire le compute quoi.
