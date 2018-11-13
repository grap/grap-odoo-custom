# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    move_to_check = fields.Boolean(
        string='Move To Check', related='move_id.to_check', store=True)

    state = fields.Selection(selection_add=[('verified', ('Verified'))])

    @api.multi
    def button_move_check(self):
        moves = self.mapped('move_id')
        moves.write({'to_check': False})

    @api.multi
    def wkf_verify_invoice(self):
        for invoice in self:
            if not invoice.date_invoice or not invoice.date_due\
                    or not invoice.supplier_invoice_number:
                raise UserError(_(
                    "Verify a supplier invoice requires to set the following"
                    " fields :\n"
                    "* 'Invoice Date';\n"
                    "* 'Due Date';\n"
                    "* 'Supplier Invoice Number';"))
        self.write({'state': 'verified'})
