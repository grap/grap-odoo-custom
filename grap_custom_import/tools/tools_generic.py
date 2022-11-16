# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def _remove_technical_keys(vals):
    res = {}
    for k, v in vals.items():
        if not k.startswith("grap_import_"):
            res[k] = v
    return res
