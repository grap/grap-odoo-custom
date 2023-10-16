# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BomPrintPurchaseListWizard(models.TransientModel):
    _name = "bom.print.purchase.list.wizard"
    _description = "Wizard for printing bill of materials"

    line_ids = fields.One2many(
        comodel_name="bom.print.purchase.list.wizard.line",
        inverse_name="wizard_id",
        string="Lines",
        default=lambda s: s._default_line_ids(),
    )

    option_group_by_product_category = fields.Boolean(
        string="Group product by product category",
        default=True,
    )

    option_display_cost = fields.Boolean(
        string="Handle products standard prices",
        default=False,
    )

    option_print_bom = fields.Boolean(
        string="Print bill of materials",
        default=False,
    )

    option_production_date = fields.Date(
        string="Production Date",
    )

    notes_for_pdf = fields.Char(
        help="Write whatever you want to be written in PDF headers"
    )

    @api.model
    def _default_line_ids(self):
        lines_vals = []
        context = self.env.context

        bom_obj = self.env["mrp.bom"]
        boms_and_quantities = context.get("boms_and_quantities", [])

        # Classic selection or button on BoMs
        if len(boms_and_quantities) == 0:
            bom_ids = context.get("active_ids", [])
            # User has selected BoMs
            if len(bom_ids) > 0:
                boms = bom_obj.browse(bom_ids)
            # User has not selected BoMs (click on action button for example)
            else:
                boms = bom_obj.search([])
            for bom in boms:
                boms_and_quantities.append({"bom": bom, "bom_qty": 1})

        # Initialize lines
        for bom_and_quantity in boms_and_quantities:
            bom = bom_and_quantity["bom"]
            _bom_description = bom_and_quantity["bom_description"]
            if bom.description_short:
                _bom_description += bom.description_short
            lines_vals.append(
                (
                    0,
                    0,
                    {
                        "bom_id": bom.id,
                        "currency_id": bom.currency_id,
                        "bom_uom_id": bom.product_uom_id,
                        "bom_description": _bom_description,
                        "bom_product_qty": bom.product_qty,
                        "quantity": bom_and_quantity["bom_qty"],
                        # standard_price_total is already divide for product unit
                        "wizard_line_subtotal": bom.standard_price_total
                        * bom_and_quantity["bom_qty"],
                    },
                )
            )
        return lines_vals

    @api.multi
    def _prepare_data(self):
        return {
            "line_data": [x.id for x in self.line_ids],
            "notes_for_pdf": self.notes_for_pdf,
            "option_group_by_product_category": self.option_group_by_product_category,
            "option_display_cost": self.option_display_cost,
            "option_print_bom": self.option_print_bom,
            "option_production_date": self.option_production_date.strftime("%d/%m/%Y")
            if self.option_production_date is not False
            else False,
        }

    @api.multi
    def print_report(self):
        self.ensure_one()
        data = self._prepare_data()
        # Get ir_actions_report
        return self.env.ref("mrp_bom_purchase.bom_purchase_list").report_action(
            self, data=data
        )
