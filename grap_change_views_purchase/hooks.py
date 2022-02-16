# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)


def configure_product_template_purchase_method(cr, registry):
    _logger.info("Configure correctly purchase_method (type in consu / product)")
    cr.execute(
        """
        UPDATE product_template
        SET purchase_method = 'receive'
        WHERE type in ('consu', 'product')
        AND (purchase_method is null or purchase_method != 'receive');
        """
    )
    _logger.info("Configure correctly purchase_method (type = service)")
    cr.execute(
        """
        UPDATE product_template
        SET purchase_method = 'purchase'
        WHERE type in ('service')
        AND (purchase_method is null or purchase_method != 'purchase');
        """
    )
