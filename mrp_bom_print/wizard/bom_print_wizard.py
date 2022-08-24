# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BomPrintWizard(models.TransientModel):
    _name = "bom.print.wizard"
    _description = "Wizard for printing bill of materials"

    line_ids = fields.One2many(
        comodel_name="bom.print.wizard.line",
        inverse_name="wizard_id",
        string="Lines",
        default=lambda s: s._default_line_ids(),
    )

    @api.model
    def _default_line_ids(self):
        lines_vals = []
        context = self.env.context
        bom_obj = self.env["mrp.bom"]
        # Get BoM
        bom_ids = context.get("active_ids", [])
        boms = bom_obj.browse(bom_ids)

        # Initialize lines
        for bom in boms:
            lines_vals.append(
                (
                    0,
                    0,
                    {
                        "bom_id": bom.id,
                        "quantity": 1,
                    },
                )
            )
        return lines_vals

    # View Section
    @api.multi
    def print_report(self):
        self.ensure_one()
        data = self._prepare_data()
        return self.env.ref("mrp_bom_print.report_bom_allergens").report_action(
            self, data=data
        )

    @api.multi
    def _prepare_data(self):
        return {
            "line_data": [x.id for x in self.line_ids],
        }

    @api.multi
    def _prepare_product_data(self):
        self.ensure_one()
        product_data = {}
        for line in self.line_ids:
            if line.product_id.id not in product_data:
                product_data[line.product_id.id] = line.quantity
            else:
                product_data[line.product_id.id] += line.quantity
        return product_data
