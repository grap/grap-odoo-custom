# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.model_create_multi
    def create(self, vals_list):
        manufacture_route_id = self.env.ref("mrp.route_warehouse0_manufacture").id
        for bom in vals_list:
            product_tmpl = self.env["product.template"].browse(
                bom.get("product_tmpl_id")
            )
            product_tmpl.write({"route_ids": [(4, manufacture_route_id)]})
        return super().create(vals_list)

    def unlink(self):
        # Get ids of following deleted products
        product_tmpl_ids = set(self.mapped("product_tmpl_id.id"))
        res = super().unlink()

        manufacture_route_id = self.env.ref("mrp.route_warehouse0_manufacture").id
        # Check if there is BoMs for theses products
        for product_tmpl_id in product_tmpl_ids:
            bom_count = self.env["mrp.bom"].search_count(
                [("product_tmpl_id", "=", product_tmpl_id)]
            )
            if bom_count == 0:
                product_tmpl = self.env["product.template"].browse(product_tmpl_id)
                # Unlink Manufacture route
                product_tmpl.write({"route_ids": [(3, manufacture_route_id)]})

        return res
