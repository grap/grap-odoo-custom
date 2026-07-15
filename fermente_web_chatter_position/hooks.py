# Copyright (C) 2026-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)


def set_default_chatter_position(cr):
    _logger.info("Configure chatter position for existing users ...")
    cr.execute("UPDATE res_users SET chatter_position = 'bottom';")
