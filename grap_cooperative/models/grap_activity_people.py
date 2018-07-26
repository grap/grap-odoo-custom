# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class GrapActivityPeople(models.Model):
    _name = 'grap.activity.people'
    _order = 'people_id'
    _rec_name = 'complete_name'

#    def name_get(self, cr, uid, ids, context=None):
#        res = []
#        for pc in self.browse(cr, uid, ids):
#            res.append((pc.id, pc.complete_name))
#        return res

    # Columns section
    activity_id = fields.Many2one(
        string='Activity', comodel_name='grap.activity',
        required=True, ondelete='cascade', readonly=True)

    people_id = fields.Many2one(
        string='People', comodel_name='grap.people',
        required=True, ondelete='cascade')

    fte = fields.Float(
        string='FTE', required=True, digits=(9, 1), default=1,
        help="Full Time Equilalent")

    working_email = fields.Char(
        string='Contact EMail', related='people_id.working_email',
        readonly=True)

    private_phone = fields.Char(
        string='Private Phone', related='people_id.private_phone',
        readonly=True)

    working_phone = fields.Char(
        string='Working Phone',
        related='people_id.grap_member_id.working_phone', readonly=True)

    complete_name = fields.Char(
        string='Name', compute='_compute_complete_name', store=True)

    # Compute Section
    @api.multi
    @api.depends('activity_id.name', 'fte')
    def _compute_complete_name(self):
        for item in self:
            item.complete_name = _(
                "%s (%s FTE" % (item.activity_id.name, item.fte))

    # Constraints section
    _sql_constraints = [
        (
            'activity_people_uniq',
            'unique(activity_id, people_id)',
            'A people can work only once time in an activity!'),
    ]
