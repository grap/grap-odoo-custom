# Copyright (C) 2019-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def configure_unit_of_measure(cr):
    _logger.info("Configure Unit of Measures ...")
    env = api.Environment(cr, SUPERUSER_ID, {})
    configuration = {
        "uom.product_uom_litre": 0.001,
        "uom.product_uom_kgm": 0.001,
        "uom.product_uom_unit": 0.001,
    }
    for xml_id, value in configuration.items():
        env.ref(xml_id).rounding = value
