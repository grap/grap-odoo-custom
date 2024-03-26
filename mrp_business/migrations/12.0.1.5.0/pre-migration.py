# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info("Migrate mrp_business code field to core code")

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mrp_bom
        SET code = ''
        WHERE code LIKE '%XX%';
    """,
    )
