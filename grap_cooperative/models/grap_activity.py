# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class GrapActivity(models.Model):
    _name = 'grap.activity'
    _inherits = {'grap.member': 'grap_member_id'}
    _order = 'activity_name'

    _STATE_SELECTION = [
        ('draft', 'No linked'),
        ('progress', 'project in progress'),
        ('validated', 'Validated'),
        ('working', 'Working'),
        ('obsolete', 'project exited'),
    ]

    # Columns section
    grap_member_id = fields.Many2one(
        string='Member', comodel_name='grap.member', required=True,
        ondelete='cascade')

    activity_name = fields.Char(string='Name', required=True)

    code = fields.Char(string='Code')

    siret = fields.Char(string='SIRET')

    vat = fields.Char(string='Taxe ID')

    web_site = fields.Char(string='Web Site')

    state = fields.Selection(
        string='State', selection=_STATE_SELECTION, required=True,
        default='draft')

    date_validated = fields.Date('Validation date by cooperative')

    date_in = fields.Date('Date of activity begins to work')

    date_out = fields.Date('Date of activity ends to work')

    type_id = fields.Many2one(string='Type', comodel_name='grap.type')

    accountant_interlocutor_id = fields.Many2one(
        string='Accoutant Interlocutor', comodel_name='grap.people')

    hr_interlocutor_id = fields.Many2one(
        string='Human Ressources Interlocutor', comodel_name='grap.people')

    attendant_interlocutor_id = fields.Many2one(
        string='Attendant Interlocutor', comodel_name='grap.people')

    category_ids = fields.Many2many(
        string='Categories', comodel_name='grap.category',
        relation='grap_activity_category_rel', column1='activity_id',
        column2='category_id')

    people_ids = fields.One2many(
        string='Workers', comodel_name='grap.activity.people',
        inverse_name='activity_id')

    fte = fields.Float(
        string='FTE', compute='_compute_fte', store=True, digits=(16, 1))

    # Compute Section
    @api.multi
    @api.depends('people_ids.activity_id', 'people_ids.fte')
    def _compute_fte(self):
        for activity in self:
            activity.fte = sum(activity.mapped('people_ids.fte'))

    # Overloads section
    @api.model
    def create(self, vals):
        vals['name'] = vals['activity_name']
        return super(GrapActivity, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'activity_name' in vals.keys():
            vals['name'] = vals['activity_name']
        return super(GrapActivity, self).write(vals)

    # Action section
    @api.multi
    def button_state_previous(self):
        for activity in self:
            for index in range(len(self._STATE_SELECTION) - 1):
                if activity.state == self._GRAP_ACTIVITY_STATE[index + 1][0]:
                    activity.state = self._GRAP_ACTIVITY_STATE[index][0]

    @api.multi
    def button_state_next(self):
        for activity in self:
            for index in range(len(self._GRAP_ACTIVITY_STATE) - 1):
                if activity.state == self._GRAP_ACTIVITY_STATE[index][0]:
                    activity.state = self._GRAP_ACTIVITY_STATE[index + 1][0]
