# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade, openupgrade_90

attachment_fields = {
    "grap.member": [
        ("image", None),
    ],
}


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade_90.convert_binary_field_to_attachment(env, attachment_fields)

    # Force to recompute image_medium and small
    for member in env["grap.member"].search([("id", "!=", 0)]):
        if member.image:
            member.write({"image": member.image})
