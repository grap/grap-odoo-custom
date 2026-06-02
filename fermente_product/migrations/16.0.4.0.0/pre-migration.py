# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

# pylint: disable=W8150
from odoo.addons.fermente_product.hooks import configure_decimal_precision


@openupgrade.migrate()
def migrate(env, version):
    configure_decimal_precision(env.cr)
