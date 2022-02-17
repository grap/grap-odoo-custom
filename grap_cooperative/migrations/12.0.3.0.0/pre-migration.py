# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

column_renames = {
    "res_company": [
        # Rename fields related to the activity
        ("accounting_interlocutor_activity_id", "accounting_referent_id"),
        ("hr_interlocutor_activity_id", "hr_referent_id"),
        ("it_interlocutor_activity_id", "it_referent_id"),
        # Rename fields related to the service team
        ("accounting_interlocutor_service_id", "accounting_interlocutor_id"),
        ("hr_interlocutor_service_id", "hr_interlocutor_id"),
        ("it_interlocutor_service_id", "it_interlocutor_id"),
        ("attendant_interlocutor_service_id", "attendant_interlocutor_id"),
    ],
}


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(env.cr, column_renames)
