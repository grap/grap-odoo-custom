# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Cooperative",
    "summary": "Add Activities, Colleges, Peoples, Members, etc.",
    "version": "12.0.2.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "base",
        "base_company_legal_info",
        "fiscal_company_base",
        "l10n_fr_siret",
        "l10n_fr_department",
        "res_company_active",
        "res_company_code",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        # "views/view_grap_activity.xml",
        "views/view_grap_activity.xml",
        # "views/view_grap_category.xml",
        "views/view_grap_college.xml",
        "views/view_grap_mandate.xml",
        # "views/view_grap_member.xml",
        "views/view_grap_people.xml",
        # "views/view_grap_type.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/grap_category.xml",
        "demo/grap_mandate.xml",
        "demo/grap_college.xml",
        "demo/grap_type.xml",
        "demo/grap_activity.xml",
        "demo/grap_people.xml",
        "demo/grap_activity_people.xml",
    ],
    "installable": True,
}
