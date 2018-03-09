# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change l10n_fr",
    "summary": "Custom changes of l10n_fr module for GRAP",
    "version": "8.0.1.0.0",
    "category": "Custom",
    "author": "GRAP",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
        "simple_tax_account",
        "l10n_fr",
    ],
    "data": [
        'views/account_tax_template.xml',
        'views/account_account_template.xml',
        'views/view_account_tax_template.xml',
    ],
}
