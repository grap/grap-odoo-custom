# Copyright 2021 Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseBatchInvoicing(models.TransientModel):
    _inherit = "purchase.batch_invoicing"

    grouping = fields.Selection(
        default="partner_id",
    )
