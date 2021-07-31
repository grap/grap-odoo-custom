# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from . import models


def preserve_translation(env, func, table_name, field_name, model_name):
    """Tools to be used in migration script
    when a field previously translated, become not translatable"""

    v = {
        "table_name": table_name,
        "field_name": field_name,
        "model_name": model_name,
    }

    # 1) Move translation value into the original field column
    sql = """
    UPDATE {v[table_name]} pp set {v[field_name]} = it.value
    FROM ir_translation it
    WHERE it.name = '{v[model_name]},{v[field_name]}'
    and it.res_id = pp.id
    and lang = 'fr_FR';
    """.format(
        v=v
    )
    func(env.cr, sql)

    # 2) Delete obsolete translations
    sql = """
    DELETE from ir_translation it
    where it.name = '{v[model_name]},{v[field_name]}'
    """.format(
        v=v
    )
    func(env.cr, sql)
