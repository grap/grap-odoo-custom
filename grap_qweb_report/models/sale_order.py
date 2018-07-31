# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def print_quotation(self):
        self.ensure_one()
        return self.env['report'].get_action(
            self, 'grap_qweb_report.grap_template_sale_order')
