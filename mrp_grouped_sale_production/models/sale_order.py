# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    grouped_order_id = fields.Many2one(
        comodel_name="mrp.grouped.sale.production",
        string="Grouped Sale Production",
        index=True,
        ondelete="cascade",
    )
