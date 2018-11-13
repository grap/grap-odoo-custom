# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models


class WizardResPartnerAddSuffixLine(models.TransientModel):
    _name = 'wizard.res.partner.add.suffix.line'
    _order = 'company_id, partner_id'

    wizard_id = fields.Many2one(
        comodel_name='wizard.res.partner.add.suffix', delete='cascade')

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner', readonly=True)

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', readonly=True)

    ebp_suffix = fields.Char(
        string='EBP Suffix', size=4)
