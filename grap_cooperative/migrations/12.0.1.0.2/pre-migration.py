# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

column_renames = {
    "grap_member": [
        ("image", None),
    ],
}


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(env.cr, column_renames)
