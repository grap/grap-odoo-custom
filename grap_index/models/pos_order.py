# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    returned_order_id = fields.Many2one(index=True)

    company_id = fields.Many2one(index=True)
