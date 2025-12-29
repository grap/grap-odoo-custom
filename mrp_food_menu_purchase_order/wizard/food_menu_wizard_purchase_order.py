# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FoodMenuWizardPurchaseOrder(models.TransientModel):
    _name = "food.menu.wizard.purchase.order"
    _description = "Wizard for launching purchase order"

    option_production_date = fields.Date(
        string="Production Date",
        default=lambda s: s._default_production_date(),
    )

    @api.model
    def _default_production_date(self):
        return self.env.context.get("production_date", False)


#     @api.model
#     def _default_line_ids(self):
#         lines_vals = []
#         context = self.env.context
#         bom_obj = self.env["mrp.bom"]
#         boms_and_quantities = context.get("boms_and_quantities", [])

#         # Classic selection or button on BoMs
#         if len(boms_and_quantities) == 0:
#             bom_ids = context.get("active_ids", [])
#             # User has selected BoMs
#             if len(bom_ids) > 0:
#                 boms = bom_obj.browse(bom_ids)
#             # User has not selected BoMs (click on action button for example)
#             else:
#                 boms = bom_obj.search([])
#             for bom in boms:
#                 boms_and_quantities.append(
#                     {
#                         "bom": bom,
#                         "bom_qty": 1,
#                         "bom_origin": "",
#                     }
#                 )

#         # Initialize lines
#         for bom_and_quantity in boms_and_quantities:
#             bom = bom_and_quantity["bom"]
#             lines_vals.append(
#                 (
#                     0,
#                     0,
#                     {
#                         "bom_id": bom.id,
#                         "currency_id": bom.currency_id,
#                         "bom_uom_id": bom.product_uom_id,
#                         "bom_origin": bom_and_quantity["bom_origin"],
#                         "bom_description": bom.description_packaging,
#                         "bom_product_qty": bom.product_qty,
#                         "quantity": bom_and_quantity["bom_qty"],
#                         # standard_price_total is already divide for product unit
#                         "wizard_line_subtotal": bom.standard_price
#                         * bom_and_quantity["bom_qty"],
#                     },
#                 )
#             )
#         return lines_vals

#     def _prepare_data(self):
#         return {
#             "currency_symbol": self.currency_id.symbol,
#             "line_data": [x.id for x in self.line_ids],
#             "title_for_pdf": self.title_for_pdf,
#             "notes_for_pdf": self.notes_for_pdf,
#             "option_group_by_product_category": self.option_group_by_product_category,
#             "option_display_cost": self.option_display_cost,
#             "option_print_bom": self.option_print_bom,
#             "option_production_date": self.option_production_date.strftime("%d/%m/%Y")
#             if self.option_production_date is not False
#             else False,
#         }

#     def print_report(self):
#         self.ensure_one()
#         data = self._prepare_data()
#         # Get ir_actions_report
#         return self.env.ref(
#             "mrp_bom_wizard_production.bom_wizard_production"
#         ).report_action(self, data=data)

# # copier coller de food menu sale order
#     # Action Section
#     def create_purchase_order_from_menu(self):
#         self.ensure_one()
#         purchase_order_line = []

#         # Prepare sale.order.line with same order
#         for line in sorted(self.menu_line_ids, key=lambda x: x.sequence):
#             futur_order_line_vals = {
#                 "sequence": line.sequence,
#                 "display_type": line.display_type,
#                 "product_id": line.product_id.id,
#                 "name": line.product_id.name if line.product_id else line.name,
#                 "product_uom_qty": line.product_uom_qty,
#                 "product_uom": line.product_uom_id.id,
#                 "price_unit": line.product_id.list_price,
#             }
#             purchase_order_line.append((0, 0, futur_order_line_vals))

#         # Return sale.order Form view with values
#         return {
#             "type": "ir.actions.act_window",
#             "res_model": "sale.order",
#             "view_mode": "form",
#             "view_type": "form",
#             "target": "current",
#             "context": {
#                 "default_partner_id": False,
#                 "default_order_line": purchase_order_line,
#                 "default_food_menu": self.id,
#             },
#         }
