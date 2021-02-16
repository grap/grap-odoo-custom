# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    cancel_msg = fields.Html(translate=False)

    done_msg = fields.Html(translate=False)

    error_msg = fields.Html(translate=False)

    name = fields.Char(translate=False)

    pending_msg = fields.Html(translate=False)

    post_msg = fields.Html(translate=False)

    pre_msg = fields.Html(translate=False)
