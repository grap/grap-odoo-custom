# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import cStringIO
import logging

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError

_logger = logging.getLogger(__name__)

try:
    from unidecode import unidecode
except ImportError:
    unidecode = False
    _logger.debug("account_export_ebp - 'unidecode' librairy not found")


class EbpExport(models.Model):
    _name = 'ebp.export'
    _order = 'date desc'

    _EBP_REMOVE_CHAR_LIST = ['\n;', ';', ',', '"']

    # Column Section
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', required=True,
        readonly=True, default=lambda s: s._default_company_id())

    fiscalyear_id = fields.Many2one(
        comodel_name='account.fiscalyear', string='Fiscal year', required=True,
        readonly=True)

    date = fields.Datetime(
        string='Date', required=True, readonly=True,
        default=lambda s: s._default_date())

    name = fields.Char(
        compute='_compute_name', string='Name', store=True, readonly=True)

    description = fields.Text(
        string='Description', readonly=True,
        help="Extra Description for Accountant Manager.")

    exported_move_qty = fields.Integer(
        oldname='exported_moves',
        string='Quantity of Moves Exported', readonly=True)

    exported_account_qty = fields.Integer(
        oldname='exported_accounts',
        string='Quantity of accounts exported', readonly=True)

    ebp_move_ids = fields.One2many(
        comodel_name='account.move', inverse_name='ebp_export_id',
        string='EBP Moves', readonly=True)

    ebp_move_qty = fields.Integer(
        compute='_compute_ebp_move_qty', string='EBP Moves Quantity',
        store=True)

    data_moves = fields.Binary(
        string='Moves file', readonly=True)

    data_accounts = fields.Binary(
        string='Accounts file', readonly=True)

    data_balance = fields.Binary(
        string='Balance file', readonly=True)

    file_name_moves = fields.Char(
        readonly=True, compute='_compute_file_name_moves')

    file_name_accounts = fields.Char(
        readonly=True, compute='_compute_file_name_accounts')

    file_name_balance = fields.Char(
        readonly=True, compute='_compute_file_name_balance')

    # Default Section
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_date(self):
        return fields.Datetime.now()

    # Compute Section
    @api.multi
    @api.depends('date')
    def _compute_name(self):
        for export in self:
            export.name = 'export_%d' % export.id

    @api.multi
    @api.depends('ebp_move_ids.ebp_export_id')
    def _compute_ebp_move_qty(self):
        for export in self:
            export.ebp_move_qty = len(export.ebp_move_ids)

    @api.multi
    def _compute_file_name_moves(self):
        for export in self:
            export.file_name_moves =\
                'export_%d_%s.csv' % (export.id, _("MOVES"))

    @api.multi
    def _compute_file_name_accounts(self):
        for export in self:
            export.file_name_accounts =\
                'export_%d_%s.csv' % (export.id, _("ACCOUNTS"))

    @api.multi
    def _compute_file_name_balance(self):
        for export in self:
            export.file_name_balance =\
                'export_%d_%s.csv' % (export.id, _("BALANCE"))

    # Custom Section
    @api.model
    def _normalize(self, text):
        res = text
        for char in self._EBP_REMOVE_CHAR_LIST:
            res = res.replace(char, " ")
        return res

    @api.multi
    def export(self, moves):
        """Export moves into 3 files and mark the moves as exported"""
        self.ensure_one()
        # Create files
        moves_file = cStringIO.StringIO()
        accounts_file = cStringIO.StringIO()
        balance_file = cStringIO.StringIO()

        # Export into files
        self._write_header_into_moves_file(moves_file)
        self._write_header_into_accounts_file(accounts_file)
        self._write_header_into_balance_file(balance_file)

        vals = self._export_to_files(
            moves, moves_file, accounts_file, balance_file)
        data_moves = base64.encodestring(moves_file.getvalue())
        data_accounts = base64.encodestring(accounts_file.getvalue())
        data_balance = base64.encodestring(balance_file.getvalue())
        moves_file.close()
        accounts_file.close()
        balance_file.close()

        # Save Datas
        vals.update({
            'data_moves': data_moves,
            'data_accounts': data_accounts,
            'data_balance': data_balance,
        })
        self.write(vals)

        # Mark moves as exported
        moves.write({
            'ebp_export_id': self.id,
        })

    @api.model
    def _export_to_files(
            self, moves, moves_file, accounts_file, balance_file):
        # dictionary to store accounts while we loop through move lines
        accounts_data = {}
        # Line counter
        i = 0

        for move in moves:
            # dictionary to summarize the lines of the move by account
            moves_data = {}
            for line in move.line_id:
                if line.credit == line.debit:
                    # Ignoring line with null debit and credit
                    continue

                account_code = self._get_account_code(move, line)
                analytic_code = self._get_analytic_code(move, line)

                move_key = (account_code, analytic_code)

                # Collect data for the file of move lines
                if move_key not in moves_data.keys():
                    moves_data[move_key] = self._prepare_move_line_dict(
                        move, line)
                else:
                    moves_data[move_key]['credit'] += line.credit
                    moves_data[move_key]['debit'] += line.debit
                    # Keep the earliest maturity date
                    if (line.date_maturity <
                            moves_data[move_key]['date_maturity']):
                        moves_data[move_key]['date_maturity'] =\
                            line.date_maturity

                # Collect data for the file of accounts
                if account_code not in accounts_data.keys():
                    accounts_data[account_code] = self._prepare_account_dict(
                        move, line)
                accounts_data[account_code]['credit'] += line.credit
                accounts_data[account_code]['debit'] += line.debit

            # Write to file
            self._write_into_moves_file(i, moves_data, moves_file)
            i += len(moves_data)

        # Write the accounts into the file
        self._write_into_accounts_file(i, accounts_data, accounts_file)

        # Write the balance of accounts into the file
        self._write_into_balance_file(i, accounts_data, balance_file)

        return {
            'exported_move_qty': len(moves),
            'exported_account_qty': len(accounts_data),
        }

    @api.model
    def _get_account_code(self, move, line):
        account = line.account_id
        company = line.company_id
        partner = line.partner_id
        res = account.code

        # Company Suffix
        if company.fiscal_company.fiscal_type == 'fiscal_mother'\
                and account.type in ('payable', 'receivable')\
                and not account.is_intercompany_trade_fiscal_company:
            res += company.code

        # Partner Suffix
        if partner and partner.ebp_suffix\
                and account.type in ('payable', 'receivable')\
                and not account.is_intercompany_trade_fiscal_company:
            res += partner.ebp_suffix

        # Tax Suffix
        if account.ebp_export_tax_code:
            if line.tax_code_id.ebp_suffix:
                # Tax code is defined
                res += line.tax_code_id.ebp_suffix
            else:
                if not account.ebp_code_no_tax:
                    raise UserError(_(
                        "The account %s - %s is set 'export with tax"
                        " suffix' but no tax suffix is defined for"
                        " the account.\n Move %s" % (
                            account.code,
                            account.name,
                            move.name)))
                else:
                    res += account.ebp_code_no_tax
        if len(res) > 10:
            # The docs from EBP state that account codes may be up to
            # 15 characters but "EBP Comptabilité" v13 will refuse anything
            # longer than 10 characters
            raise UserError(_(
                "Account code '%s' is too long to be exported to"
                " EBP.") % res)
        return res

    @api.model
    def _get_analytic_code(self, move, line):
        res = ''
        if line.account_id.ebp_analytic_mode == 'fiscal_analytic':
            res = line.company_id.code
        elif line.account_id.ebp_analytic_mode == 'normal':
            if line.analytic_account_id:
                res = line.analytic_account_id.code
            elif line.company_id.ebp_default_analytic_account_id:
                res =\
                    line.company_id.ebp_default_analytic_account_id.code
        return res

    @api.model
    def _prepare_move_line_dict(self, move, line):

        if move.partner_id.intercompany_trade:
            ref = ' (' + move.partner_id.name + ')'
        else:
            ref = (
                line.name +
                ((' (' + move.ref + ')')
                    if move.ref else ''))

        # Manage analytic cases
        if line.account_id.ebp_analytic_mode == 'fiscal_analytic':
            ref = line.company_id.code + ' ' + ref

        return {
            'date': move.date,
            'journal': move.journal_id.ebp_code,
            'account_code': self._get_account_code(move, line),
            'ref': self._normalize(ref),
            'name': self._normalize(move.name),
            'credit': line.credit,
            'debit': line.debit,
            'date_maturity': line.date_maturity,
            'currency_name': move.company_id.currency_id.name,
            'analytic_code': self._get_analytic_code(move, line),
        }

    @api.model
    def _write_header_into_moves_file(self, moves_file):
        # Move File header
        data = [
            _("Line"),
            _("Date"),
            _("Journal Code"),
            _("Account Number"),
            _("Name"),
            _("Move Number"),
            _("Amount (related to the direction)"),
            _("Direction"),
            _("Due Date"),
            _("Currency"),
            _("Analytic Account"),
        ]
        self._write_into_file(data, moves_file)

    @api.model
    def _write_into_moves_file(self, count, moves_data, moves_file):
        i = count

        for key, line in moves_data.iteritems():
            i += 1
            data = [
                # Line number
                '%d' % i,
                # Date (ddmmyy)
                '%s/%s/%s' % (
                    line['date'][8:10], line['date'][5:7],
                    line['date'][2:4]),
                # Journal
                self._normalize(line['journal'])[:4],
                # Account number
                # (possibly with the partner code appended to it)
                line['account_code'],
                # Manual title
                '"%s"' % line['ref'][:40],
                # Accountable receipt number
                '"%s"' % line['name'][:15],
            ]
            if line['credit']:
                data += [
                    # Amount
                    '%f' % abs(line['credit']),
                    # [C]redit or [D]ebit
                    'C',
                ]
            else:
                data += [
                    # Amount
                    '%f' % abs(line['debit']),
                    # [C]redit or [D]ebit
                    'D',
                ]
            data += [
                # Date of maturity (ddmmyy)
                line['date_maturity'] and '%s%s%s' % (
                    line['date_maturity'][8:10],
                    line['date_maturity'][5:7],
                    line['date_maturity'][2:4]) or '',
                # Currency
                line['currency_name'],
            ]
            data += [
                line['analytic_code'],
            ]
            self._write_into_file(data, moves_file)

    @api.model
    def _prepare_account_dict(self, move, line):
        res = {
            'name': '',
            'partner_name': '',
            'address': '',
            'zip': '',
            'city': '',
            'country': '',
            'contact': '',
            'phone': '',
            'fax': '',
            'credit': 0,
            'debit': 0,
            'allow_analytic': '',
            'payment_mode': 'CH30',
            'rgpd': 'N',
        }

        if (line.partner_id and line.partner_id.ebp_suffix and
                line.account_id.type in ('payable', 'receivable')):
            # Partner account
            if line.account_id.\
                    is_intercompany_trade_fiscal_company:
                partner = line.company_id.partner_id
            else:
                partner = line.partner_id
            res.update({
                'name': self._normalize(partner.name),
                'partner_name': self._normalize(partner.name),
                'address': self._normalize(
                    (partner.street or '') +
                    (partner.street2 and
                        (' ' + partner.street2) or '')),
                'zip': partner.zip or '',
                'city': self._normalize(partner.city or ''),
                'country': self._normalize(
                    partner.country_id.name or ''),
                'contact': self._normalize(partner.email or ''),
                'phone': partner.phone or partner.mobile or '',
                'fax': partner.fax or '',
            })
        elif (line.account_id.ebp_export_tax_code and
                line.tax_code_id.ebp_suffix):
            res.update({
                'name': (
                    self._normalize(line.account_id.name) +
                    '(' + self._normalize(line.tax_code_id.name) + ')'),
            })
        else:
            # Normal account
            res.update({
                'name': self._normalize(line.account_id.name),
            })

        if line.account_id.ebp_analytic_mode in ['fiscal_analytic', 'normal']:
            res.update({
                'allow_analytic': '1',
            })

        return res

    @api.model
    def _write_header_into_accounts_file(self, accounts_file):
        pass

    @api.model
    def _write_into_accounts_file(self, count, accounts_data, accounts_file):
        for account_code, account_data in accounts_data.iteritems():
            data = [
                self._normalize(account_code),
                self._normalize(account_data['name'])[:60],
                self._normalize(account_data['partner_name'])[:30],
                self._normalize(account_data['address'])[:100],
                self._normalize(account_data['zip'])[:5],
                self._normalize(account_data['city'])[:30],
                self._normalize(account_data['country'])[:35],
                self._normalize(account_data['contact'])[:35],
                self._normalize(account_data['phone'])[:20],
                self._normalize(account_data['fax'])[:20],
                account_data['allow_analytic'],
                account_data['payment_mode'],
                account_data['rgpd'],

            ]
            self._write_into_file(data, accounts_file)

    @api.model
    def _write_header_into_balance_file(self, balance_file):
        # Move File header
        data = [
            _("Account Number"),
            _("Account name"),
            _("Debit"),
            _("Credit"),
            _("Debit Balance"),
            _("Credit Balance"),
        ]
        self._write_into_file(data, balance_file)

    @api.model
    def _write_into_balance_file(self, count, accounts_data, balance_file):
        for account_code, account_data in accounts_data.iteritems():
            credit = (account_data['credit'] or 0)
            debit = (account_data['debit'] or 0)
            if credit > debit:
                credit_balance = credit - debit
                debit_balance = 0
            else:
                credit_balance = 0
                debit_balance = debit - credit
            data = [
                account_code.replace(',', ''),
                (account_data['name'] or '').replace(',', '')[:60],
                str(debit),
                str(credit),
                str(debit_balance),
                str(credit_balance),
            ]
            self._write_into_file(data, balance_file)

    @api.model
    def _write_into_file(self, data_list, file):
        tmp = ','.join(data_list)
        file.write(unidecode(tmp))
        file.write('\r\n')

    #     _logger.debug(
    #         "%d accounts(s) exported to COMPTES.TXT" % len(accounts_data))

    #     self.write(cr, uid, ids, {
    #         'exported_moves': len(exported_move_ids),
    #         'ignored_moves': len(ignored_move_ids),
    #         'exported_lines': l,
    #         'exported_accounts': len(accounts_data),
    #     }, context=context)
    #     if export_id:
    #         export_obj.write(cr, uid, export_id, {
    #             'exported_moves': len(exported_move_ids),
    #             'ignored_moves': len(ignored_move_ids),
    #             'exported_lines': l,
    #             'exported_accounts': len(accounts_data),
    #         }, context=context)
    #     return export_id

# FILE
# FUCK ANALYTIC

    #     is_analytic_column = False
    #     for move in moves:
    #         if move.company_id.ebp_trigram != '':
    #             is_analytic_column = True

        # if is_analytic_column:
        #     move_line += ',Poste analytique'

    # AH BON ????
    #             if len(move.name) > 15:
    #                 raise osv.except_osv(_('Move name too long'), _(
    #                     """Move name '%s' is too long to be exported to"""
    #                     """ EBP.""") % move.name)
