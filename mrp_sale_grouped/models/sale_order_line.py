# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sale_grouped_display_name = fields.Char(
        compute="_compute_sale_grouped_display_name",
        help="Technical field, used to display matrix"
        " with web_widget_x2many_2d_matrix module.",
    )

    @api.multi
    def _compute_sale_grouped_display_name(self):
        for sale_order_line in self:
            sale_order_line.sale_grouped_display_name = (
                sale_order_line.order_id.name
                + " "
                + sale_order_line.order_partner_id.name
            )
