# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info("Migrate mrp_business description fields to mrp_bom_note field notes")

    if not openupgrade.column_exists(env.cr, "mrp_bom", "notes"):
        _logger.info("If mrp_bom_note was not installed, create column")
        openupgrade.logged_query(
            env.cr,
            """
            ALTER TABLE mrp_bom
            ADD COLUMN notes text;
            """,
        )

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mrp_bom
        SET notes = '<p>' || description_short || '<br/>' || description_long || '</p>';
    """,
    )
