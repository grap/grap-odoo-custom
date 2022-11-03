# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    product_tmpl_code = fields.Char(related="product_tmpl_id.default_code")

    product_tmpl_name = fields.Char(related="product_tmpl_id.name")

    def see_current_product_from_supplierinfo(self):
        self.ensure_one()
        result = self.env.ref(
            "grap_change_views_product.action_product_product"
        ).read()[0]
        form_view = self.env.ref("grap_change_views_product.view_product_product_form")
        result["views"] = [(form_view.id, "form")]
        # Get product id → first product variant
        product_template = self.env["product.template"].search(
            [("id", "=", self.product_tmpl_id.id)]
        )
        product = product_template.product_variant_ids[0]
        result["res_id"] = product.id
        result["context"] = {
            "form_view_initial_mode": "edit",
        }
        return result
