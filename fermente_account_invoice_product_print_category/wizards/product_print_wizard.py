# Copyright (C) 2026-Today GRAP (http://www.grap.coop)
# @author Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductPrintWizard(models.TransientModel):
    _inherit = "product.print.wizard"

    @api.model
    def _default_line_ids(self):
        lines_vals = []
        context = self.env.context
        AccountMove = self.env["account.move"]
        if context.get("active_model", False) == "account.move":
            move_ids = AccountMove.search([("id", "in", context.get("active_ids", []))])
            products = move_ids.mapped("invoice_line_ids.product_id")

            for product in products:
                lines_vals.append(
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "print_category_id": product.print_category_id.id,
                            "quantity": 1,
                        },
                    )
                )

        else:
            lines_vals = super()._default_line_ids()
        return lines_vals
