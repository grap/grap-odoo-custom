# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.logging()
def _create_hr_employee_from_grap_people(env):
    env.cr.execute(
        """
        SELECT * from grap_people;
        """
    )
    columns = [col[0] for col in env.cr.description]
    rows = [dict(zip(columns, row)) for row in env.cr.fetchall()]  # noqa: B905
    for row in rows:
        if not row["company_id"]:
            continue

        # We don't recover private information
        # (private_phone / address)
        vals = {
            "firstname": row["first_name"],
            "lastname": row["last_name"],
            "work_email": row["working_email"],
            "mobile_phone": row["working_phone"],
            "company_id": row["company_id"],
            "birthday": row["birthdate"],
        }

        if row["working_email"]:
            user = (
                env["res.users"]
                .sudo()
                .search(
                    [
                        ("login", "not ilike", "-eboutique"),
                        ("login", "not ilike", "_caisse"),
                        ("login", "not ilike", "-TI"),
                        ("email", "=", row["working_email"]),
                    ]
                )
                .filtered(lambda x: len(x.login) != 3)
            )
            if len(user) == 1:
                vals["user_id"] = user.id
            elif len(user) > 1:
                _logger.warning(f"Many users found for email {row['working_email']}...")

        _logger.info(f"Creating {row['first_name']} {row['last_name']} employee ...")
        _logger.info(vals)
        employee = env["hr.employee"].with_company(row["company_id"]).create(vals)

        attachment = env["ir.attachment"].search(
            [
                ("res_model", "=", "grap.people"),
                ("res_field", "=", "image"),
                ("res_id", "=", row["id"]),
            ]
        )

        if attachment:
            _logger.info(
                f"Transfer image (#{attachment.id})"
                f"from grap.people#{row['id']}"
                f" ({row['first_name']} / {row['last_name']}) "
                f" to new hr.employee#{employee.id} ..."
            )

            openupgrade.logged_query(
                """UPDATE ir_attachment
                set res_id = %s
                res_model = 'hr.employee'
                res_field = 'image_1920'
                """,
                (employee.id,),
            )
            employee.image_1920 = employee.image_1920


@openupgrade.migrate()
def migrate(env, version):
    _create_hr_employee_from_grap_people(env)
