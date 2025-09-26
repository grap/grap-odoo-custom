# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # Commenté en attendant de rebosser sérieusement sur le sujet
    # des prix HT, TTC sur le prix unitaire, total autant sur
    # Odoo que sur les PDF, dans account et sale
    # price_total_displayed = fields.Monetary(
    #     string="Amount (w / wo taxes)", compute="_compute_price_total_displayed"
    # )

    # def _compute_price_total_displayed(self):
    #     for line in self:
    #         price_include = any(line.mapped("tax_ids.price_include"))
    #         if price_include:
    #             line.price_total_displayed = line.price_total
    #         else:
    #             line.price_total_displayed = line.price_subtotal
