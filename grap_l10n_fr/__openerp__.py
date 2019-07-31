# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change l10n_fr",
    "summary": "Custom changes of l10n_fr module for GRAP",
    "version": "8.0.2.0.0",
    "category": "Custom",
    "author": "GRAP",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
        "l10n_fr",
        "account_export_ebp",
        "account_product_fiscal_classification_usage_group",
    ],
    "data": [
        'data/account_tax_template.xml',
        'data/account_account_template.xml',
        'data/account_tax_code_template.xml',
        'data/account_chart_template.xml',
        'data/account_fiscal_position_template.xml',
        'data/account_fiscal_position_tax_template.xml',
        'data/account_product_fiscal_classification_template.xml',
        'views/view_account_tax_template.xml',
        'views/view_account_tax_code_template.xml',
    ],
    'installable': False,
}
