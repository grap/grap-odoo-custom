# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BomWizardRangeBomLine(models.TransientModel):
    _name = "bom.wizard.range.bom.line"
    _description = "Wizard line of actual boms range"

    # Columns Section
    wizard_id = fields.Many2one(comodel_name="bom.wizard.create.range")
    bom_id = fields.Many2one(comodel_name="mrp.bom")
    packaging = fields.Many2one(related="bom_id.packaging")
