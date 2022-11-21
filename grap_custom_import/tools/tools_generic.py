# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def _str_to_float(value):
    """Harmonize float values"""
    return float(str(value).replace(",", ".").replace(" ", ""))


def _str_percent_to_float(value):
    """Harmonize percent fields. if a field is a percent
    two values possible in the csv / excel files:
    - "0,2"
    - "20,0%"
    The function will return a float 0.2 in all cases
    """
    if not value:
        return
    if "%" in value:
        return _str_to_float(str(value).replace("%", "")) / 100
    return _str_to_float(value)


def _str_monetary_to_float(value):
    """Harmonize monetary fields. if a field is a percent
    two values possible in the csv / excel files:
    - "0,2"
    - "20,0%"
    The function will return a float 0.2 in all cases
    """
    if not value:
        return
    return _str_to_float(str(value).replace("€", ""))


def _remove_technical_keys(vals):
    res = {}
    for k, v in vals.items():
        if not k.startswith("grap_import_"):
            res[k] = v
    return res
