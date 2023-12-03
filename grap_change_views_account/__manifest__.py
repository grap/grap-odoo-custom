# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Quentin DUPONT <quentin.dupont@grap.coop>
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Views Account",
    "version": "12.0.1.1.15",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "account",
        "sale",
        # OCA
        "account_financial_report",
        "account_group_menu",
        "account_invoice_overdue_reminder",
        "account_invoice_supplier_ref_unique",
        "account_invoice_supplierinfo_update_qty_multiplier",
        "account_invoice_triple_discount",
        "account_subsequence_fiscal_year",
        "web_tree_dynamic_colored_field",
        # GRAP
        "account_invoice_supplierinfo_update_standard_price",
    ],
    "data": [
        "views/menu.xml",
        "views/view_account_account.xml",
        "views/view_account_account_template.xml",
        "views/view_account_account_type.xml",
        "views/view_account_invoice.xml",
        "views/view_account_journal.xml",
        "views/view_account_move.xml",
        "views/view_account_tax_group.xml",
        "wizards/view_overdue_reminder_start.xml",
        "wizards/view_wizard_update_invoice_supplierinfo.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
    ],
    "installable": True,
}
