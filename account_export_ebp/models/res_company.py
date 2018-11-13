# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # Column Section
    ebp_analytic_enabled = fields.Boolean(
        string='Enable Analytic in EBP', default=False,
        help="Check this box if you want to enable the analytic when"
        " exporting in EBP. Note that this setting has will not been"
        " taken into account for Companies that belong to a CAE")

    ebp_default_analytic_account_id = fields.Many2one(
        string="Default Analytic Account for EBP",
        comodel_name='account.analytic.account')
