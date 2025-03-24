# Copyright (C) 2019-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def configure_decimal_precision(cr):
    _logger.info("Configure Decimal precision")
    env = api.Environment(cr, SUPERUSER_ID, {})
    configuration = {
        "product.decimal_stock_weight": 3,
        "product.decimal_volume": 3,
    }
    for xml_id, value in configuration.items():
        env.ref(xml_id).digits = value
