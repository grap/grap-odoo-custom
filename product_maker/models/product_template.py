# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    maker_description = fields.Char(
        string="Maker",
        compute=lambda x: x._compute_template_field_from_variant_field(
            "maker_description"
        ),
        inverse=lambda x: x._set_product_variant_field("maker_description"),
        readonly=False,
    )
