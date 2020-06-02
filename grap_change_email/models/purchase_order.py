# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def wkf_send_rfq(self):
        """Return the custom GRAP template"""
        res = super(PurchaseOrder, self).wkf_send_rfq()
        template = self.env.ref(
            "grap_change_email.email_template_purchase_order"
        )
        res["context"].update(
            {
                "default_use_template": bool(template.id),
                "default_template_id": template.id,
            }
        )
        return res
