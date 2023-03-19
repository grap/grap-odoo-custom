# Copyright 2020 Druidoo - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    env.cr.execute(
        """
        SELECT id, name
        FROM res_company
        ORDER BY id;"""
    )
    company_datas = env.cr.fetchall()
    for (company_id, company_name) in company_datas:
        env.cr.execute(
            """
            SELECT ia.id
            FROM ir_attachment ia
            INNER JOIN account_invoice ai
                ON ia.res_id = ai.id
                AND ia.res_model = 'account.invoice'
            WHERE ai.type in ('in_invoice', 'in_refund')
            AND ai.company_id = %s""",
            (company_id,),
        )
        attachment_datas = env.cr.fetchall()
        if attachment_datas:
            _logger.info(
                "Unlinking %d attachments for supplier invoices for the company %d - %s"
                % (len(attachment_datas), company_id, company_name)
            )
            attachment_ids = [x[0] for x in attachment_datas]
            attachments = env["ir.attachment"].browse(attachment_ids)
            attachments.with_context(intercompany_trade_create=True).unlink()
