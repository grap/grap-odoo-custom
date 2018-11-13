# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    _SEARCH_DATE_BEGIN = '01/12/2012'

    # Columns section
    ebp_suffix = fields.Char(
        string="Suffix in EBP", oldname="ref_nb",
        help="When exporting Entries to EBP, this suffix will be"
        " appended to the Account Number to make it a Partner Account.")

    has_ebp_move_line = fields.Boolean(
        compute='_compute_has_ebp_move_line',
        search='_search_has_ebp_move_line',
        string='Has Account Move Lines exportable in EBP')

    # Constraints section
    _sql_constraints = [
        (
            'ebp_suffix_company_id_uniq',
            'unique (ebp_suffix, company_id)',
            'The EBP suffix must be unique per company!')
    ]

    # Columns section
    @api.multi
    def _compute_has_ebp_move_line(self):
        AccountMoveLine = self.env['account.move.line']
        for partner in self:
            partner.has_ebp_move_line = len(AccountMoveLine.search([
                ('partner_id', '=', partner.id),
                ('date', '>=', self._SEARCH_DATE_BEGIN)]))

    @api.model
    def _search_has_ebp_move_line(self, operator, value):
        assert operator in ('=', '!='), 'Invalid domain operator'
        assert value in (True, False), 'Invalid domain value'

        with_line = (
            (operator == '=' and value is True) or
            (operator == '!=' and value is False))

        self._cr.execute(
            "SELECT partner_id, count(*)"
            " FROM account_move_line"
            " WHERE date >= '01/12/2012'"
            " GROUP BY partner_id"
            " HAVING  count(*) > 0")
        res = self._cr.fetchall()
        return [('id', with_line and 'in' or 'not in', [x[0] for x in res])]
