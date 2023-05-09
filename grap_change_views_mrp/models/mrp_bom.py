# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    product_name = fields.Char(related="product_id.name")
    #
    # override to make it related to product_id (and not product_tmpl_id)
    # as it's related to product_id and required with this module
    product_uom_id = fields.Many2one(
        related="product_id.uom_id",
    )

    product_finished = fields.Boolean(
        string="Finished product",
        related="product_id.sale_ok",
    )

    product_intermediate = fields.Boolean(
        string="Intermediate product",
        related="product_id.is_intermediate",
    )
