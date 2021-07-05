# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

from odoo.addons.grap_change_translation import preserve_translation


@openupgrade.migrate()
def migrate(env, version):
    preserve_translation(
        env, openupgrade.logged_query, "product_pricelist", "name", "product.pricelist"
    )
