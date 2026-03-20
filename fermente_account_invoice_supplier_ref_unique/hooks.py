# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)


def _hook_enable_for_existing_company(cr, registry):
    _logger.info(
        "[fermente_account_invoice_supplier_ref_unique]"
        " Initialize check_invoice_supplier_number"
    )
    cr.execute("""UPDATE res_company set check_invoice_supplier_number = true""")
