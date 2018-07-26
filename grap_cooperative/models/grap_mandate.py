# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class GrapMandate(models.Model):
    _name = 'grap.mandate'

    name = fields.Char(string='Name', required=True)

    people_ids = fields.Many2many(
        string='Members', comodel_name='grap.people',
        relation='grap_people_mandate_rel', column1='mandate_id',
        column2='people_id')

    people_qty = fields.Integer(
        string='People count', compute='_compute_people_qty', store=True)

    @api.multi
    @api.depends('people_ids')
    def _compute_people_qty(self):
        for item in self:
            item.people_qty = len(item.people_ids)
