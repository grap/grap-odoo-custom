# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BarcodeNomenclature(models.Model):
    _inherit = "barcode.nomenclature"

    active = fields.Boolean(string="active", default=True)
