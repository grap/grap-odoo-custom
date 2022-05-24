# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # Doing with Product and not product template
    product_tmpl_id = fields.Many2one(
        "product.template",
        "Product",
        related="product_id.product_tmpl_id",
        required=True,
    )

    product_id = fields.Many2one(
        "product.product",
        "Product Variant",
        domain="[('type', 'in', ['product', 'consu'])]",
        required=True,
    )


# Erreurs à l'installation
# 2022-05-24 09:39:52,591 147248 WARNING mrp_food2 odoo.models: method mrp.bom._check_product_recursion: @constrains parameter 'product_tmpl_id' is not writeable
# 2022-05-24 09:39:52,591 147248 WARNING mrp_food2 odoo.models: method mrp.bom.check_kit_has_not_orderpoint: @constrains parameter 'product_tmpl_id' is not writeable
# 2022-05-24 09:39:53,576 147248 WARNING mrp_food2 odoo.modules.loading: Table 'mrp_bom': column 'product_id': unable to set constraint NOT NULL
# column "product_id" contains null values
