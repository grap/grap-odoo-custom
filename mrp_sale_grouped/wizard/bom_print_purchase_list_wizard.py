# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import UserError


class BomPrintPurchaseListWizard(models.TransientModel):
    _inherit = "bom.print.purchase.list.wizard"

    @api.model
    def _default_no_origin(self):
        context = self.env.context
        active_model = context.get("active_model")
        if active_model == "mrp.sale.grouped":
            sale_grouped_active_id = context.get("active_ids", [])
            sale_grouped_obj = self.env["mrp.sale.grouped"]
            sale_grouped_obj.browse(sale_grouped_active_id)

            # Handle production_date
            no_origin = False
        else:
            no_origin = True

        return super(
            BomPrintPurchaseListWizard,
            self.with_context(context, no_origin=no_origin),
        )._default_no_origin()

    @api.model
    def _default_title_for_pdf(self):
        context = self.env.context

        active_model = context.get("active_model")
        if active_model == "mrp.sale.grouped":
            sale_grouped_active_id = context.get("active_ids", [])
            sale_grouped_obj = self.env["mrp.sale.grouped"]
            sale_grouped = sale_grouped_obj.browse(sale_grouped_active_id)

            # Handle production_date
            title_for_pdf = sale_grouped.name
        else:
            title_for_pdf = False

        return super(
            BomPrintPurchaseListWizard,
            self.with_context(context, title_for_pdf=title_for_pdf),
        )._default_title_for_pdf()

    @api.model
    def _default_notes(self):
        context = self.env.context

        active_model = context.get("active_model")
        if active_model == "mrp.sale.grouped":
            sale_grouped_active_id = context.get("active_ids", [])
            sale_grouped_obj = self.env["mrp.sale.grouped"]
            sale_grouped = sale_grouped_obj.browse(sale_grouped_active_id)

            # Handle production_date
            notes_for_pdf = sale_grouped.notes
        else:
            notes_for_pdf = False

        return super(
            BomPrintPurchaseListWizard,
            self.with_context(context, notes_for_pdf=notes_for_pdf),
        )._default_notes()

    @api.model
    def _default_production_date(self):
        context = self.env.context

        active_model = context.get("active_model")
        if active_model == "mrp.sale.grouped":
            sale_grouped_active_id = context.get("active_ids", [])
            sale_grouped_obj = self.env["mrp.sale.grouped"]
            sale_grouped = sale_grouped_obj.browse(sale_grouped_active_id)

            # Handle production_date
            production_date = sale_grouped.date
        else:
            production_date = False

        return super(
            BomPrintPurchaseListWizard,
            self.with_context(context, production_date=production_date),
        )._default_production_date()

    @api.model
    def _default_line_ids(self):
        context = self.env.context
        active_model = context.get("active_model")

        if active_model == "mrp.sale.grouped":
            sale_grouped_active_id = context.get("active_ids", [])
            sale_grouped_obj = self.env["mrp.sale.grouped"]
            sale_grouped = sale_grouped_obj.browse(sale_grouped_active_id)
            order_ids = sale_grouped.mapped("order_ids")

            missing_boms = []
            boms_and_quantities = {}

            for order in order_ids:
                for order_line in order.order_line:
                    if not order_line.product_id.bom_ids:
                        missing_boms.append(order_line.product_id.name)
                    else:
                        bom = order_line.product_id.bom_ids[0]
                        bom_qty = order_line.product_uom_qty
                        if bom.id in boms_and_quantities:
                            boms_and_quantities[bom.id]["bom_qty"] += bom_qty
                            boms_and_quantities[bom.id]["bom_origin"] += (
                                ", " + order.name
                            )
                        else:
                            boms_and_quantities[bom.id] = {
                                "bom": bom,
                                "bom_qty": bom_qty,
                                "bom_origin": order.name,
                            }

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
        else:
            boms_and_quantities = []

        return super(
            BomPrintPurchaseListWizard,
            self.with_context(context, boms_and_quantities=boms_and_quantities),
        )._default_line_ids()
