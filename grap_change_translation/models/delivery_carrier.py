# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    description = fields.Text(translate=False)

    description_picking = fields.Text(translate=False)

    description_purchase = fields.Text(translate=False)

    description_sale = fields.Text(translate=False)

    name = fields.Char(translate=False)
