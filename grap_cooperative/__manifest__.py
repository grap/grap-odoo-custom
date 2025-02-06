# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Cooperative",
    "summary": "Add Directories, Companies, Colleges, Peoples, etc.",
    "version": "16.0.2.0.0",
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
        "social_media_mastodon",
        "social_media_gitlab",
        "web_view_leaflet_map",
        # GRAP
        "fiscal_company_base",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/view_hr_employee_global.xml",
        "views/view_res_company.xml",
        "views/view_res_company_category.xml",
    ],
    "demo": [
        "demo/hr_employee.xml",
    ],
    "installable": True,
}
