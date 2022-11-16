# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import models

from ..tools import tools_generic, tools_partner

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Overload Section
    def _load_records_create(self, vals_list):
        _logger.info("====================================")
        _logger.info("====================================")
        _logger.info("====================================")
        _logger.info("_load_records_create")
        _logger.info("INITIAL VALUES : %d items" % len(vals_list))
        _logger.info(vals_list)
        new_vals_list = []
        for vals in vals_list:
            new_vals = vals.copy()
            new_vals = tools_partner._handle_partner_name(self, new_vals)
            new_vals = tools_generic._remove_technical_keys(new_vals)
            new_vals_list.append(new_vals)
        _logger.info("====================================")
        _logger.info("FINAL VALUES : %d items" % len(new_vals_list))
        _logger.info(new_vals_list)
        products = super()._load_records_create(new_vals_list)
        return products
