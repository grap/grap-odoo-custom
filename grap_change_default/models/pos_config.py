# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    iface_gross_weight_method = fields.Selection(default="manual")

    iface_tax_included = fields.Selection(default="total")

    iface_create_confirmed_sale_order = fields.Boolean(default=False)

    cash_control = fields.Boolean(default=True)

    max_meal_voucher_amount = fields.Monetary(default=19.0)

    module_account = fields.Boolean(default=True)

    invoice_journal_id = fields.Many2one(default=False)
