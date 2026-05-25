# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# pylint: disable=W8150
from odoo.addons.fermente_cooperative_directory import hooks


def migrate(cr, version):
    hooks._hide_technical_employees(cr)
