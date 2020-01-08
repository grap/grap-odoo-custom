# Copyright (C) 2018-Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    invoice_extra_cost = fields.Boolean(
        default=False,
        string="Invoice - Extra cost",
        help="For a sale order, display its price at the bottom of the invoice,\
         above the total",
    )
