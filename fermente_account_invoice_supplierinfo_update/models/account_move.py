# Copyright 2026-Today: GRAP (https://www.grap.coop)
# Copyright Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    # View Section
    def go_to_products_view(self):
        self.ensure_one()
        products = self.mapped("invoice_line_ids.product_id.product_tmpl_id")
        action = self.env.ref("product.product_template_action").sudo().read()[0]
        action["domain"] = [("id", "in", products.ids)]
        action["views"] = [
            (self.env.ref("product.product_template_tree_view").id, "tree"),
            (self.env.ref("product.product_template_form_view").id, "form"),
        ]
        return action
