# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BomWizardRangePackagingLine(models.TransientModel):
    _name = "bom.wizard.range.packaging.line"
    _description = "Wizard line to create range"

    # Columns Section
    wizard_id = fields.Many2one(comodel_name="bom.wizard.create.range")
    product_id = fields.Many2one(
        comodel_name="product.product",
        domain="[('is_packaging', '=', True)]",
    )
