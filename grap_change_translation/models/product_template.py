# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    description = fields.Char(translate=False)

    description_picking = fields.Char(translate=False)

    description_pickingin = fields.Char(translate=False)

    description_pickingout = fields.Char(translate=False)

    description_purchase = fields.Char(translate=False)

    description_sale = fields.Char(translate=False)

    name = fields.Char(translate=False)
