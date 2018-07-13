# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class GrapMember(models.Model):
    _name = 'grap.member'
    _order = 'name'

    # Columns section
    name = fields.Char(string='Name', readonly=True)

    image = fields.Binary(string='Image')

    street = fields.Char(string='Street', size=128)

    zip = fields.Char(string='Zip')

    city = fields.Char(string='City')

    working_email = fields.Char(string='Contact EMail')

    working_phone = fields.Char(string='Working Phone')

    college_id = fields.Many2one(
        string='College', comodel_name='grap.college')

    date_capital_entry = fields.Date(string='Entry date In Capital')

    share_number = fields.Integer(string='Number of Share in Capital')

    # Overload section
#    def name_get(self, cr, uid, ids, context=None):
#        return super(GrapMember, self).name_get(cr, uid, ids, context=context)

#    def name_search(
#            self, cr, uid, name='', args=None, operator='ilike',
#            context=None, limit=100):
#        return super(grap_member, self).name_search(
#            cr, uid, name=name, args=args, operator=operator,
#            context=context, limit=limit)
