# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'GRAP - Change Precision',
    'version': '8.0.1.0.0',
    'summary': 'Change the precisions names and values of some fields',
    'category': 'Custom',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'purchase',
        'point_of_sale',
        'standard_price_vat_included',
    ],
    'data': [
        'data/decimal_precision.xml',
    ],
}
