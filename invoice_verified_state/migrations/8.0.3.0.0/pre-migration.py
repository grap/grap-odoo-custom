# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

__name__ = u"Precompute 'move_to_check' field of account_invoice"


def precompute_move_to_check(cr):
    sql = """
    ALTER TABLE account_invoice ADD COLUMN move_to_check BOOLEAN;
    UPDATE account_invoice ai
    SET move_to_check = am.to_check
    FRoM account_move am
    WHERE ai.move_id = am.id;
    """
    cr.execute(sql)


def migrate(cr, version):
    if not version:
        return
    precompute_move_to_check(cr)
