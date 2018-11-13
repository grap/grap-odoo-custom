# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "GRAP - Export accounting moves to EBP",
    'version': '8.0.3.0.0',
    'author': 'Numérigraphe SARL,GRAP',
    'category': 'GRAP - Custom',
    'license': 'AGPL-3',
    'depends': [
        'account_accountant',
        'base_fiscal_company',
        'intercompany_trade_fiscal_company',
    ],
    'external_dependencies': {
        'python': ['unidecode'],
    },
    'data': [
        'security/ir_model_access.yml',
        'security/ir_rule.xml',
        'views/menu.xml',
        'wizard/view_wizard_res_partner_add_suffix.xml',
        'wizard/view_wizard_ebp_export.xml',
        'wizard/view_wizard_ebp_unexport.xml',
        'views/view_account_account.xml',
        'views/view_account_journal.xml',
        'views/view_account_move.xml',
        'views/view_account_tax_code.xml',
        'views/view_ebp_export.xml',
        'views/view_res_partner.xml',
        'views/view_res_company.xml',
    ],
    'demo': [
        'demo/account_journal.xml',
    ],
    'installable': True,
}
