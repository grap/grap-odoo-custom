# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP for Food",
    "summary": "MRP modules adapted for food-related professions",
    "version": "12.0.1.1.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # OCA modules
        # peut-être à enlever, utile juste pour le code automatique du bom
        "res_company_code",
        # GRAP modules,
    ],
    "data": [
        "views/view_mrp_bom.xml",
    ],
    "installable": True,
}
