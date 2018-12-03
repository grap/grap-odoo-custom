# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Point Of Sale - Change Sale Move Lines',
    'version': '8.0.1.0.0',
    'category': 'Point Of Sale',
    'author': 'GRAP',
    'summary': 'Make Sale accounting moves from PoS acceptable for accoutants',
    'depends': [
        'pos_pricelist',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/account_account.xml',
        'demo/account_tax_code.xml',
        'demo/account_tax.xml',
        'demo/product_product.xml',
    ],
    'installable': True,
}
