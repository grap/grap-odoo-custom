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

    option_allergens_only_code = fields.Boolean(
        string="Display allergen code instead of their name",
        default=False,
    )

    option_allergens_only_code_text = fields.Char(
        compute="_compute_option_allergens_only_code_text",
    )

    @api.model
    def _default_line_ids(self):
        lines_vals = []
        context = self.env.context
        bom_obj = self.env["mrp.bom"]
        # Get BoM
        bom_ids = context.get("active_ids", [])
        # User has selected BoMs
        if len(bom_ids) > 0:
            boms = bom_obj.browse(bom_ids)
        # User has not selected BoMs (click on action button for example)
        else:
            boms = bom_obj.search([])

        # Initialize lines
        for bom in boms:
            lines_vals.append(
                (
                    0,
                    0,
                    {
                        "bom_id": bom.id,
                        "bom_allergens_ids": bom.bom_allergen_ids,
                    },
                )
            )
        return lines_vals

    @api.multi
    def print_report(self):
        self.ensure_one()
        data = self._prepare_data()
        # Get ir_actions_report bom_allergens
        return self.env.ref("mrp_bom_print.bom_allergens").report_action(
            self, data=data
        )

    @api.multi
    def _prepare_data(self):
        return {
            "line_data": [x.id for x in self.line_ids],
            "option_allergens_only_code": self.option_allergens_only_code,
            "option_allergens_only_code_text": self.option_allergens_only_code_text,
        }

    # Compute Section
    def _compute_option_allergens_only_code_text(self):
        allergens_all = self.env["product.allergen"].search([])
        self.option_allergens_only_code_text = ""
        for allergen in allergens_all.filtered(lambda x: x.code):
            self.option_allergens_only_code_text += (
                str(allergen.code) + " : " + str(allergen.name) + " - "
            )
        self.option_allergens_only_code_text = self.option_allergens_only_code_text[:-3]
