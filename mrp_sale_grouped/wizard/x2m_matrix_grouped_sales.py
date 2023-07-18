# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class X2mMatrixGroupedSalesWizard(models.TransientModel):
    _name = "x2m.matrix.grouped.sales.wizard"
    _description = "X2Many Matrix Grouped Sales Wizard"

    line_ids = fields.Many2many(
        comodel_name="sale.order.line",
        default=lambda self: self._default_line_ids(),
        relation="x2m_matrix_grouped_sales_wizard_line_rel",
    )

    def _default_line_ids(self):
        grouped_sale_prod = self.env["mrp.sale.grouped"].browse(
            self.env.context.get("active_id")
        )
        return grouped_sale_prod.mapped("order_ids.order_line")

    def save_close(self):
        return
