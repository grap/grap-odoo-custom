# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'GRAP - Change Accesses',
    'version': '8.0.1.0.0',
    'category': 'GRAP - Custom',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'email_template',
        'delivery',
        'product',
        'stock',
        'point_of_sale',
        'base',
        'purchase',
        'sale',
        'procurement',
        'account_fiscal_company',
        'crm',
        'calendar',
    ],
    'data': [
        'security/ir_module_category.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
