# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):

    # Fill new field product_qty_net
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mrp_bom_line SET product_qty_net = product_qty;
        """,
    )
