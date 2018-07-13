# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'GRAP - Cooperative',
    'version': '8.0.2.0.0',
    'category': 'GRAP - Custom',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/view_grap_activity.xml',
        'views/view_grap_category.xml',
        'views/view_grap_college.xml',
        'views/view_grap_mandate.xml',
        'views/view_grap_member.xml',
        'views/view_grap_people.xml',
        'views/view_grap_type.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/grap_activity.xml',
        'demo/grap_people.xml',
        'demo/grap_activity_people.xml',
    ],
}
