# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BomWizardProduction(models.TransientModel):
    _inherit = "bom.wizard.production"

    missing_boms_text = fields.Char(
        default=lambda s: s._default_missing_boms_text(),
    )

    def _get_food_menu_from_context(self):
        return self.env["mrp.food.menu"].browse(self.env.context.get("active_ids", []))

    # Set PDF Title with food_menu Title
    @api.model
    def _default_title_for_pdf(self):
        context = self.env.context

        if context.get("active_model") == "mrp.food.menu":
            food_menu = self._get_food_menu_from_context()
            title_for_pdf = food_menu.name
        else:
            title_for_pdf = False

        return super(
            BomWizardProduction,
            self.with_context(context, title_for_pdf=title_for_pdf),
        )._default_title_for_pdf()

    # # Set PDF notes with food_menu Notes
    # @api.model
    # def _default_notes(self):
    #     context = self.env.context

    #     if context.get("active_model") == "mrp.food.menu":
    #         food_menu = self._get_food_menu_from_context()
    #         notes_for_pdf = food_menu.notes
    #     else:
    #         notes_for_pdf = False

    #     return super(
    #         BomWizardProduction,
    #         self.with_context(context, notes_for_pdf=notes_for_pdf),
    #     )._default_notes()

    # Set PDF production date with food_menu production date
    # @api.model
    # def _default_production_date(self):
    #     context = self.env.context

    #     if context.get("active_model") == "mrp.food.menu":
    #         food_menu = self._get_food_menu_from_context()
    #         production_date = food_menu.date
    #     else:
    #         production_date = False

    #     return super(
    #         BomWizardProduction,
    #         self.with_context(context, production_date=production_date),
    #     )._default_production_date()

    # @api.model
    def _default_missing_boms_text(self):
        context = self.env.context

        if context.get("active_model") == "mrp.food.menu":
            food_menu = self._get_food_menu_from_context()
            # Get name (with size limit) of products without any BoM
            missing_boms_text = ", ".join(
                food_menu.product_wo_bom_ids.mapped("display_name")
            )[:30]
        else:
            missing_boms_text = ""

        return missing_boms_text

    # Override method to add "Origin" field that precise Sales linked to BoM
    @api.model
    def _default_line_ids(self):
        context = self.env.context

        if context.get("active_model") == "mrp.food.menu":
            food_menu = self._get_food_menu_from_context()
            menu_line_ids = food_menu.mapped("menu_line_ids")

            missing_boms = {}
            boms_and_quantities = {}

            for menu_line in menu_line_ids.filtered(lambda x: not x.display_type):
                if not menu_line.bom_id:
                    missing_boms[menu_line.bom_id] = menu_line.product_id.name
                else:
                    bom = menu_line.bom_id
                    bom_qty = menu_line.product_uom_qty
                    if bom.id in boms_and_quantities:
                        boms_and_quantities[bom.id]["bom_qty"] += bom_qty
                        boms_and_quantities[bom.id]["bom_origin"] += (
                            ", " + menu_line.name
                        )
                    else:
                        boms_and_quantities[bom.id] = {
                            "bom": bom,
                            "bom_qty": bom_qty,
                            "bom_origin": menu_line.name,
                        }

            # Change boms_and_quantities for the expected format
            boms_and_quantities = list(boms_and_quantities.values())

        else:
            boms_and_quantities = []

        return super(
            BomWizardProduction,
            self.with_context(context, boms_and_quantities=boms_and_quantities),
        )._default_line_ids()
