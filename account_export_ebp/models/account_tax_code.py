# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class AccountTaxCode(models.Model):
    _inherit = 'account.tax.code'

    _SEARCH_DATE_BEGIN = '01/01/2017'

    # Columns section
    ebp_suffix = fields.Char(
        string="Suffix in EBP", oldname="ref_nb",
        help="When exporting Entries to EBP, this suffix will be"
        " appended to the Account Number to make it a new Account.")

    has_ebp_suffix_required = fields.Boolean(
        compute='_compute_has_ebp_suffix_required',
        search='_search_has_ebp_suffix_required',
        string='Require EBP Suffix')

    # Columns section
    @api.multi
    def _compute_has_ebp_suffix_required(self):
        res = self._get_has_ebp_suffix_required()
        for code in self:
            for item in res:
                if item[0] == code.id:
                    code.has_ebp_suffix_required = True
                    continue

    @api.multi
    def _get_has_ebp_suffix_required(self):
        # pylint: disable=sql-injection
        req = """
            SELECT aml.tax_code_id, count(*)
            FROM account_move_line aml
            INNER JOIN account_account aa
             ON aa.id = aml.account_id
            WHERE aa.ebp_export_tax_code is True
            AND tax_code_id in %s
            AND aml.date >= '%s'
            GROUP BY aml.tax_code_id
        """ % (tuple(self.ids), self._SEARCH_DATE_BEGIN)
        self._cr.execute(req)
        res = self._cr.fetchall()
        return res

    @api.model
    def _search_has_ebp_suffix_required(self, operator, value):
        assert operator in ('=', '!='), 'Invalid domain operator'
        assert value in (True, False), 'Invalid domain value'

        with_line = (
            (operator == '=' and value is True) or
            (operator == '!=' and value is False))

        # Get ids accessible in the current context
        res = self.search([])._get_has_ebp_suffix_required()
        return [('id', with_line and 'in' or 'not in', [x[0] for x in res])]
