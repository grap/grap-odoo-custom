# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Account - Invoice 'Verified' state",
    'version': '7.0.1.0.0',
    'category': 'Accounting',
    'description': """
Add a 'Verified' state on account.invoice
=========================================

* Add a Verified state on account.invoice;
* Only Account_manager can validate supplier account.invoice;
* Modify the corresponding workflow;

Copyright, Author and Licence
-----------------------------

* Copyright : 2013, Groupement Régional Alimentaire de Proximité;
* Author :
    * Julien WESTE;
* Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_voucher',
    ],
    'data': [
        'views/account_invoice_view.xml',
        'views/account_journal_view.xml',
        'data/workflow.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
    ],
}
