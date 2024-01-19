# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BomPrintPurchaseListWizard(models.TransientModel):
    _inherit = "bom.print.purchase.list.wizard"

    missing_boms_text = fields.Char(
        default=lambda s: s._default_missing_boms_text(),
    )

    def _get_sale_grouped_from_context(self):
        return self.env["mrp.sale.grouped"].browse(
            self.env.context.get("active_ids", [])
        )

    @api.model
    def _default_no_origin(self):
        context = self.env.context

        if context.get("active_model") == "mrp.sale.grouped":
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

        if context.get("active_model") == "mrp.sale.grouped":
            sale_grouped = self._get_sale_grouped_from_context()
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

        if context.get("active_model") == "mrp.sale.grouped":
            sale_grouped = self._get_sale_grouped_from_context()
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

        if context.get("active_model") == "mrp.sale.grouped":
            sale_grouped = self._get_sale_grouped_from_context()
            production_date = sale_grouped.date
        else:
            production_date = False

        return super(
            BomPrintPurchaseListWizard,
            self.with_context(context, production_date=production_date),
        )._default_production_date()

    @api.model
    def _default_missing_boms_text(self):
        context = self.env.context

        if context.get("active_model") == "mrp.sale.grouped":
            sale_grouped = self._get_sale_grouped_from_context()
            # Get name of products without any BoM
            missing_boms_text = ", ".join(
                sale_grouped.product_wo_bom_ids.mapped("display_name")
            )
        else:
            missing_boms_text = False

        return missing_boms_text

    @api.model
    def _default_line_ids(self):
        context = self.env.context

        if context.get("active_model") == "mrp.sale.grouped":
            sale_grouped = self._get_sale_grouped_from_context()
            order_ids = sale_grouped.mapped("order_ids")

            missing_boms = {}
            boms_and_quantities = {}

            for order in order_ids:
                for order_line in order.order_line.filtered(
                    lambda x: not x.display_type
                ):
                    if not order_line.product_id.bom_ids:
                        missing_boms[order_line.product_id] = order_line.product_id.name
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

        else:
            boms_and_quantities = []

        return super(
            BomPrintPurchaseListWizard,
            self.with_context(context, boms_and_quantities=boms_and_quantities),
        )._default_line_ids()
