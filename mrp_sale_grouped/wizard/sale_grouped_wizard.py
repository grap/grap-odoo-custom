# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleGroupedWizard(models.TransientModel):
    _name = "sale.grouped.wizard"
    _description = "Wizard for printing Production Plan"

    line_ids = fields.One2many(
        comodel_name="sale.grouped.wizard.line",
        inverse_name="wizard_id",
        string="Lines",
        default=lambda s: s._default_line_ids(),
    )

    @api.model
    def _default_line_ids(self):
        lines_vals = []
        context = self.env.context
        sale_order_obj = self.env["mrp.sale.grouped"]
        # Get sale_order
        sale_order_ids = context.get("active_ids", [])
        # User has selected sales_orders
        if len(sale_order_ids) > 0:
            sales_orders = sale_order_obj.browse(sale_order_ids).mapped("order_ids")
        # User has not selected sales_orders (click on action button for example)
        else:
            sales_orders = sale_order_obj.search([]).mapped("order_ids")

        # Initialize lines
        for sale_order in sales_orders:
            lines_vals.append(
                (
                    0,
                    0,
                    {
                        "sale_id": sale_order.id,
                        "sale_partner_id": sale_order.partner_id.id,
                        # "currency_id": sale_order.currency_id,
                        # "sale_order_uom_id": sale_order.product_uom_id,
                        # "sale_order_description": sale_order.description_short,
                        # "sale_order_product_qty": sale_order.product_qty,
                        # "quantity": sale_order.product_qty,
                        # "wizard_line_subtotal": sale_order.standard_price_total,
                    },
                )
            )
        return lines_vals

    @api.multi
    def _prepare_data(self):
        return {
            "line_data": [x.sale_id.id for x in self.line_ids],
            # "notes_for_pdf": self.notes_for_pdf,
            # "option_group_by_product_category": self.option_group_by_product_category,
            # "option_display_cost": self.option_display_cost,
            # "option_print_sale_order": self.option_print_sale_order,
            # "option_production_date": self.option_production_date.strftime(
            #     "%A %-d %B %Y"
            # )
            # if self.option_production_date is True
            # else False,
        }

    @api.multi
    def print_report(self):
        self.ensure_one()
        data = self._prepare_data()
        # Get ir_actions_report
        return self.env.ref("mrp_sale_grouped.report_sale_grouped").report_action(
            self, data=data
        )
