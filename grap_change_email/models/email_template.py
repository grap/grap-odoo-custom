# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class EmailTemplate(models.Model):
    _inherit = 'email.template'

    active = fields.Boolean(string='active', default=True)

    @api.multi
    def disable_useless_template(self):
        self.write({'active': False})
