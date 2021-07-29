# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    _PARTNER_TYPE_SELECTION = [
        ("customer", "Customer"),
        ("supplier", "Supplier"),
        ("customer_supplier", "Customer and supplier"),
    ]

    partner_type_selec = fields.Selection(
        string="Partner type",
        selection=_PARTNER_TYPE_SELECTION,
        required=True,
    )

    # Compute Section
    @api.onchange("partner_type_selec")
    def onchange_supplier_customer(self):
        for partner in self:
            if partner.partner_type_selec == "customer":
                partner.customer = True
                partner.supplier = False
            elif partner.partner_type_selec == "supplier":
                partner.customer = False
                partner.supplier = True
            elif partner.partner_type_selec == "customer_supplier":
                partner.customer = True
                partner.supplier = True
