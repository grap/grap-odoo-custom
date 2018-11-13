# coding: utf-8
# Copyright (C) 2013-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "GRAP - Invoices 'Verified' / 'To Check' state",
    'version': '8.0.3.0.0',
    'category': 'Custom',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_voucher',
    ],
    'data': [
        'views/view_account_invoice.xml',
        'views/view_account_journal.xml',
        'data/workflow.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
}
