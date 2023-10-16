# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import UserError


class BomPrintPurchaseListWizard(models.TransientModel):
    _inherit = "bom.print.purchase.list.wizard"

    @api.model
    def _default_line_ids(self):
        context = self.env.context
        boms_and_quantities = {}

        active_model = context.get("active_model")
        if active_model == "mrp.sale.grouped":
            sale_grouped_active_id = context.get("active_ids", [])
            sale_grouped_obj = self.env["mrp.sale.grouped"]
            sale_grouped = sale_grouped_obj.browse(sale_grouped_active_id)
            order_ids = sale_grouped.mapped("order_ids")

            missing_boms = []

            for order in order_ids:
                for order_line in order.order_line:
                    if not order_line.product_id.bom_ids:
                        missing_boms.append(order_line.product_id.name)
                    else:
                        bom = order_line.product_id.bom_ids[0]
                        bom_qty = order_line.product_qty
                        if bom.id in boms_and_quantities:
                            boms_and_quantities[bom.id]["bom_qty"] += bom_qty
                            boms_and_quantities[bom.id]["bom_description"] += (
                                ", " + order.name
                            )
                        else:
                            boms_and_quantities[bom.id] = {
                                "bom": bom,
                                "bom_qty": bom_qty,
                                "bom_description": "From " + order.name,
                            }

            for _bom_id, _bom_data in boms_and_quantities.items():
                _bom_data["bom_description"] += ". "

            # Change boms_and_quantities for the expected format
            boms_and_quantities = list(boms_and_quantities.values())

            if missing_boms:
                boms_text = ", ".join(missing_boms)
                message = (
                    "These products don't have any Bill Of Material: "
                    + boms_text
                    + "\nCreate them before launching the assistant again."
                )
                raise UserError(message)

        return super(
            BomPrintPurchaseListWizard,
            self.with_context(context, boms_and_quantities=boms_and_quantities),
        )._default_line_ids()
