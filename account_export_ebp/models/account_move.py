# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Column Section
    ebp_export_id = fields.Many2one(
        comodel_name='ebp.export', old_name='exported_ebp_id',
        string='EBP Export', copy=False,
        help="Indicates whether the move has already been exported"
        " to EBP or not. It is changed automatically.")

    # Override section
    @api.multi
    def write(self, vals):
        self._check_exported_moves()
        return super(AccountMove, self).write(vals)

    @api.multi
    def unlink(self):
        self._check_exported_moves()
        return super(AccountMove, self).unlink()

    # Custom section
    @api.multi
    def _check_exported_moves(self):
        if not self.env.context.get('force_write_ebp_exported', False):
            exported_moves =\
                self.filtered(lambda x: x.ebp_export_id.id is not False)
            if exported_moves:
                raise UserError(_(
                    "You cannot modify or delete exported moves: %s!")
                    % ', '.join([m.name for m in exported_moves]))
