# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(env.cr, "product_product", "is_intermediate"):
        openupgrade.logged_query(
            env.cr,
            """
            ALTER TABLE product_product
            ADD COLUMN is_intermediate boolean;
            """,
        )

    # is_intermediate
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_product
        SET is_intermediate = (SELECT CASE WHEN EXISTS (
            SELECT 1
            FROM mrp_bom_line
            WHERE mrp_bom_line.product_id = product_product.id
            )
            AND EXISTS (
                SELECT 1 FROM mrp_bom WHERE product_id = product_product.id
                )
            THEN True ELSE False END);
        """,
    )
    # is_component
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_product
        SET is_component = (SELECT CASE WHEN EXISTS (
            SELECT 1
            FROM mrp_bom_line
            WHERE mrp_bom_line.product_id = product_product.id
            ) AND NOT EXISTS (
                SELECT 1
                FROM mrp_bom
                WHERE product_id = product_product.id
                )
            THEN True ELSE False END);
        """,
    )
