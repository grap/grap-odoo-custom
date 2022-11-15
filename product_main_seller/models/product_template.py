# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # QuickFIX : Fields from a older version of this module
    # Had to let them, otherwise Odoo throws an error
    main_seller_partner_id = fields.Boolean(help="Deprecated")
    main_seller_variant_partner_id = fields.Boolean(help="Deprecated")
