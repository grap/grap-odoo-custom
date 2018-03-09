# -*- coding: utf-8 -*-
# Copyright 2017, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "GRAP Change l10n_fr",
    "summary": "Module summary",
    "version": "8.0.1.0.0",
    "category": "Uncategorized",
    "author": "GRAP",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
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
