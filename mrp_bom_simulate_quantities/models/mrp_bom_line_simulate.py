# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpBomLineSimulate(models.Model):
    _name = "mrp.bom.line.simulate"
    _description = "Simulated BoM Line"

    bom_id = fields.Many2one(comodel_name="mrp.bom", string="BoM")

    product_id = fields.Many2one(comodel_name="product.product", string="Product")

    product_qty = fields.Float(string="Quantity")

    product_uom_id = fields.Many2one(comodel_name="uom.uom", string="Unit of Measure")
