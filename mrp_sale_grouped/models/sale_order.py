# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mrp_sale_grouped_id = fields.Many2one(
        comodel_name="mrp.sale.grouped",
        string="Grouped Sale Production",
        index=True,
    )
