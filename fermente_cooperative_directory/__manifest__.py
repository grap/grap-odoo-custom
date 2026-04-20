# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - Cooperative Directory",
    "summary": "Add Directories for companies and employees",
    "version": "16.0.3.2.2",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "hr",
        "social_media",
        # OCA
        "base_geolocalize_company",
        "base_fontawesome",
        "hr_employee_firstname_partner_firstname",
        "l10n_fr_siret",
        "l10n_fr_department",
        "res_company_active",
        "res_company_category",
        "res_company_code",
        "res_company_mastodon_link",
        "res_company_gitlab_link",
        "web_view_leaflet_map",
        # GRAP
        "fiscal_company_base",
        "hr_direct_address_home",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/view_hr_employee.xml",
        "views/view_hr_employee_global.xml",
        "views/view_res_company.xml",
        "views/view_res_company_category.xml",
    ],
    "demo": [
        "demo/hr_employee.xml",
    ],
    "installable": True,
}
