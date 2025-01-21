# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info("=== Drop obsolete view to avoid error on migration")
    openupgrade.logged_query(
        env.cr,
        """
        DELETE from ir_ui_view where id in (
            SELECT res_id from ir_model_data where module='mrp_business'
            AND name = 'view_mrp_business_bom_form'
        );
    """,
    )
