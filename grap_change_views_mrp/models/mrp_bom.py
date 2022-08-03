# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    product_name = fields.Char(related="product_id.name")

    # override to make it related to product_id (and not product_tmpl_id)
    # as it's related to product_id and required with this module
    product_uom_id = fields.Many2one(
        "uom.uom",
        "Product Unit of Measure",
        related="product_id.uom_id",
        oldname="product_uom",
        required=True,
    )
