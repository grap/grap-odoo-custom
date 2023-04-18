# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from psycopg2.extensions import AsIs

logger = logging.getLogger(__name__)


def drop_indexes(cr, registry):
    indexes = {
        "account_bank_statement_line": ["pos_statement_id"],
        "pos_order": ["returned_order_id", "company_id"],
        "pos_order_line": ["order_id"],
        "stock_move": ["created_purchase_line_id", "inventory_id"],
        "stock_move_line": ["picking_id"],
        "stock_picking": ["group_id", "sale_id"],
    }

    for table_name, field_names in indexes.items():
        for field_name in field_names:
            index_name = "%s_%s_index" % (table_name, field_name)
            logger.info("dropping posgresql index %s" % index_name)
            cr.execute("DROP INDEX IF EXISTS %s;", (AsIs(index_name),))
