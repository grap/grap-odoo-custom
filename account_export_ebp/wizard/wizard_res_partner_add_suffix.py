# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp import api, fields, models

_logger = logging.getLogger(__name__)

try:
    from unidecode import unidecode
except ImportError:
    unidecode = False
    _logger.debug("account_export_ebp - 'unidecode' librairy not found")


class WizardResPartnerAddSuffix(models.TransientModel):
    _name = 'wizard.res.partner.add.suffix'

    line_ids = fields.One2many(
        comodel_name='wizard.res.partner.add.suffix.line',
        inverse_name='wizard_id', string='Lines')

    # View Section
    @api.multi
    def button_affect_suffix(self):
        for wizard in self:
            for line in wizard.line_ids:
                if line.ebp_suffix:
                    line.partner_id.write({'ebp_suffix': line.ebp_suffix})

    # Overloading section
    @api.model
    def default_get(self, default_fields):
        ResPartner = self.env['res.partner']

        res = super(
            WizardResPartnerAddSuffix, self).default_get(default_fields)

        line_ids = []

        selected_partner_ids = self.env.context.get('active_ids', [])
        if not selected_partner_ids:
            return res
        existing_suffixes = {}
        sql_req = """
            SELECT rp.company_id, rp.ebp_suffix from res_partner rp
            WHERE ebp_suffix is not Null """
        self.env.cr.execute(sql_req)
        result = self.env.cr.dictfetchall()
        for item in result:
            existing_suffixes.setdefault(item['company_id'], [])
            existing_suffixes[item['company_id']] += [item['ebp_suffix']]

        for partner in ResPartner.browse(selected_partner_ids):
            if partner.ebp_suffix:
                ebp_suffix = partner.ebp_suffix
            else:
                ebp_suffix = self._get_suffix(
                    partner.name, existing_suffixes.get(
                        partner.company_id.id, []))
                if ebp_suffix:
                    existing_suffixes.setdefault(partner.company_id.id, [])
                    existing_suffixes[partner.company_id.id] += [ebp_suffix]
            line_ids.append((0, 0, {
                'partner_id': partner.id,
                'company_id': partner.company_id.id,
                'ebp_suffix': ebp_suffix,
            }))
        res.update({'line_ids': line_ids})
        return res

    # Private Section
    @api.model
    def _get_suffix(self, name, existing_suffixes):
        # remove special caracters
        name2 = ''.join(e for e in name if e.isalnum())
        # if nothing remains, return False
        if not name2:
            return False
        # first try: return the 4 fisrt caracters
        suffix = name2[:min(4, len(name2))].upper()
        suffix = unidecode(suffix)
        if suffix and not(suffix in existing_suffixes):
            return suffix
        # second try: look for different words in the name
        # and try taking caracters from them
        for sep in [' ', """'""", '-']:
            if sep in name:
                names = name.split(sep)
                for i in range(0, len(names)):
                    names[i] = ''.join(e for e in names[i] if e.isalnum())
                for j in range(1, len(names)):
                    for n in range(3, 0, -1):
                        if len(names[0]) >= n:
                            suffix = (
                                names[0][:n].upper() +
                                names[j][:(4 - n)].upper())
                            suffix = unidecode(suffix)
                            if suffix and not(suffix in existing_suffixes):
                                return suffix
        # third try: takes first 3 caracters and add a one digit number
        for x in range(2, 10):
            suffix = name2[:min(3, len(name2))].upper() + str(x)
            suffix = unidecode(suffix)
            if suffix and not(suffix in existing_suffixes):
                return suffix
        # fourth try: takes first 2 caracters and add a two digit number
        for x in range(10, 100):
            suffix = name2[:min(2, len(name2))].upper() + str(x)
            suffix = unidecode(suffix)
            if suffix and not(suffix in existing_suffixes):
                return suffix
        # fifth try: takes first 1 caracters and add a three digit number
        for x in range(100, 1000):
            suffix = name2[:1].upper() + str(x)
            suffix = unidecode(suffix)
            if suffix and not(suffix in existing_suffixes):
                return suffix
        return False
