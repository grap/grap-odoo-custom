# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Account Invoice Supplier Ref Unique",
    "version": "16.0.1.0.0",
    "category": "Web",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": ["account_invoice_supplier_ref_unique"],
    "data": [],
    "post_init_hook": "_hook_enable_for_existing_company",
}
