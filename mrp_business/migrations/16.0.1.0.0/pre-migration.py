# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info(
        "=== Migrate mrp_bom.time_to_produce → product_template.produce_delay_in_hour"
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_template pt
        SET produce_delay_in_hour = mb.time_to_produce
        FROM mrp_bom mb
        WHERE mb.product_tmpl_id = pt.id
          AND mb.time_to_produce IS NOT NULL;

    """,
    )
    _logger.info("=== Set onchange values produce_delay_in_hour")
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_template
        SET produce_delay = produce_delay_in_hour / 24;
    """,
    )
