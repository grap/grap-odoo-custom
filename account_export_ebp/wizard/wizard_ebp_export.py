# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class WizardEbpExport(models.TransientModel):
    _name = "wizard.ebp.export"

    _STATE_SELECTION = [
        ('draft', 'Draft'),
        ('done', 'Done'),
    ]

    # Columns Section
    ebp_export_id = fields.Many2one(
        string='EBP Export', comodel_name='ebp.export', readonly=True)

    state = fields.Selection(
        selection=_STATE_SELECTION, string='State', default='draft')

    fiscalyear_id = fields.Many2one(
        comodel_name='account.fiscalyear', string='Fiscal year',
        required=True, default=lambda s: s._default_fiscalyear_id(),
        domain="[('state', '=', 'draft')]",
        help='Only the moves in this fiscal year will be exported')

    description = fields.Text(
        string='Description',
        help="Extra Description for Accountant Manager.")

    file_name_moves = fields.Char(
        related='ebp_export_id.file_name_moves', readonly=True)

    file_name_accounts = fields.Char(
        related='ebp_export_id.file_name_accounts', readonly=True)

    file_name_balance = fields.Char(
        related='ebp_export_id.file_name_balance', readonly=True)

    data_moves = fields.Binary(
        related='ebp_export_id.data_moves', readonly=True)

    data_accounts = fields.Binary(
        related='ebp_export_id.data_accounts', readonly=True)

    data_balance = fields.Binary(
        related='ebp_export_id.data_balance', readonly=True)

    ignored_draft_move_qty = fields.Integer(
        compute='_compute_move_selection', multi='move_selection',
        store=True)

    ignored_period_move_qty = fields.Integer(
        compute='_compute_move_selection', multi='move_selection',
        store=True)

    ignored_journal_code_move_qty = fields.Integer(
        compute='_compute_move_selection', multi='move_selection',
        store=True)

    ignored_to_check_move_qty = fields.Integer(
        compute='_compute_move_selection', multi='move_selection',
        store=True)

    ignored_exported_move_qty = fields.Integer(
        compute='_compute_move_selection', multi='move_selection',
        store=True)

    ignored_partner_move_qty = fields.Integer(
        compute='_compute_move_selection', multi='move_selection',
        store=True)

    ignored_tax_code_move_qty = fields.Integer(
        compute='_compute_move_selection', multi='move_selection',
        store=True)

    selected_move_qty = fields.Integer(
        string='Quantity of Selected Moves', readonly=True,
        compute='_compute_move_selection', multi='move_selection',
        store=True)

    exported_move_ids = fields.Many2many(
        string='Exported Moves', comodel_name='account.move',
        compute='_compute_move_selection', multi='move_selection',
        store=True)

    exported_move_qty = fields.Integer(
        string='Quantity of Exported Moves', readonly=True,
        compute='_compute_move_selection', multi='move_selection',
        store=True)

    # Default Section
    @api.model
    def _default_fiscalyear_id(self):
        AccountMove = self.env['account.move']
        moves = AccountMove.browse(self.env.context.get('active_ids', []))
        fiscalyears = moves.mapped('period_id.fiscalyear_id')
        if len(fiscalyears) == 1:
            return fiscalyears[0].id
        else:
            return False

    @api.multi
    @api.depends('fiscalyear_id')
    def _compute_move_selection(self):
        AccountMove = self.env['account.move']
        AccountJournal = self.env['account.journal']

        for wizard in self:
            selected_moves = AccountMove.browse(
                self.env.context.get('active_ids', []))
            wizard.selected_move_qty = len(selected_moves)

            selection_domain = [
                ('id', 'in', self.env.context.get('active_ids', []))]
            full_domain = selection_domain[:]

            # filter by state (remove draft)
            wizard.ignored_draft_move_qty = len(AccountMove.search(
                selection_domain + [('state', '=', 'draft')]))
            full_domain += [('state', '!=', 'draft')]

            # Filter by partner without ebp suffix
            without_correct_partner_move_lines =\
                selected_moves.mapped('line_id').filtered(
                    lambda x: x.partner_id and
                    x.partner_id.has_ebp_move_line is False)
            without_correct_partner_move_ids =\
                without_correct_partner_move_lines.mapped('move_id').ids
            wizard.ignored_partner_move_qty =\
                len(without_correct_partner_move_ids)
            full_domain +=\
                [('id', 'not in', without_correct_partner_move_ids)]

            # Filter by tax code without ebp suffix
            without_correct_tax_code_move_lines =\
                selected_moves.mapped('line_id').filtered(
                    lambda x: x.tax_code_id and
                    x.tax_code_id.has_ebp_move_line is False)
            without_correct_tax_code_move_ids =\
                without_correct_tax_code_move_lines.mapped('move_id').ids
            wizard.ignored_tax_code_move_qty =\
                len(without_correct_tax_code_move_ids)
            full_domain +=\
                [('id', 'not in', without_correct_tax_code_move_ids)]

            # filter by period (from fiscalyear)
            if self.fiscalyear_id:
                periods = self.fiscalyear_id.period_ids
                wizard.ignored_period_move_qty = len(AccountMove.search(
                    selection_domain +
                    [('period_id', 'not in', periods.ids)]))
                full_domain += [('period_id', 'in', periods.ids)]

            # Filter by journal (ebp_code should be defined)
            journals = AccountJournal.search([('ebp_code', '!=', False)])
            wizard.ignored_journal_code_move_qty = len(AccountMove.search(
                selection_domain + [('journal_id', 'not in', journals.ids)]))
            full_domain += [('journal_id', 'in', journals.ids)]

            # filter moves to check
            wizard.ignored_to_check_move_qty = len(AccountMove.search(
                selection_domain + [('to_check', '=', True)]))
            full_domain += [('to_check', '=', False)]

            # filter yet exported moves
            wizard.ignored_exported_move_qty = len(AccountMove.search(
                selection_domain + [('ebp_export_id', '!=', False)]))
            full_domain += [('ebp_export_id', '=', False)]

            wizard.exported_move_ids = AccountMove.search(full_domain)
            wizard.exported_move_qty = len(wizard.exported_move_ids.ids)

    @api.multi
    def button_export(self):
        self.ensure_one()
        EbpExport = self.env['ebp.export']
        self.ebp_export_id = EbpExport.create({
            'fiscalyear_id': self.fiscalyear_id.id,
            'description': self.description,
        })
        self._compute_move_selection()
        self.ebp_export_id.export(self.exported_move_ids)
        self.state = 'done'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.ebp.export',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
            'context': {},
        }
