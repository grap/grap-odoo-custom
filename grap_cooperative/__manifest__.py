# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Cooperative",
    "summary": "Add Directories, Companies, Colleges, Peoples, etc.",
    "version": "12.0.3.1.0",
    "development_status": "Alpha",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "social_media",
        # OCA
        "base_geolocalize_company",
        "l10n_fr_siret",
        "l10n_fr_department",
        "res_company_active",
        "res_company_category",
        "res_company_code",
        "web_view_leaflet_map",
        # GRAP
        "base_company_legal_info",
        "fiscal_company_base",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/view_grap_college.xml",
        "views/view_grap_mandate.xml",
        "views/view_grap_people.xml",
        "views/view_res_company.xml",
        "views/view_res_company_category.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/grap_mandate.xml",
        "demo/grap_college.xml",
        "demo/grap_people.xml",
    ],
    "installable": True,
}
