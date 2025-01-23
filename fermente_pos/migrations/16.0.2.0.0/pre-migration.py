# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info("Set pos picking management as real time for all companies.")
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_company
        SET point_of_sale_update_stock_quantities = 'real';
    """,
    )
