# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    product_name = fields.Char(related="product_tmpl_id.name")

    product_finished = fields.Boolean(
        string="Finished product",
        related="product_tmpl_id.sale_ok",
    )

    product_intermediate = fields.Boolean(
        string="Intermediate product",
        related="product_tmpl_id.is_intermediate",
    )
