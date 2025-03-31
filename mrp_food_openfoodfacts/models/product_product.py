# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
from odoo import api, fields, models
from openfoodfacts import openfoodfacts

class ProductProduct(models.Model):
    _inherit = "product.product"

    # API Documentation https://openfoodfacts.github.io/openfoodfacts-python/Usage
    @api.model
    def _get_product_in_off_database(self):
        query = {}
        if self.barcode:
            res = openfoodfacts.products.get_product(self.barcode)
            res_product = res['product']
            res_name = res_product['product_name']
            print("======== AVEC CODE BARRE ==========")
        else:
            query["search_terms"] = self.name
            res = openfoodfacts.products.advanced_search(query)
            res_product = res['products'][0]
            res_name = res_product['product_name']
            print("======== AVEC NOM ==========")
        # import pdb; pdb.set_trace()
        print("=============>>>>>>>>>>>>" +  res_name)
        return res_product

    @api.model
    def _set_product_allergens(self, product_off):
        # Get product allergens_tags
        product_off_allergens = product_off['allergens_tags']
        # Get company allergens
        allergens_obj = self.env["product.allergen"]
        # for each allergens_tags, chercher l'équivalent
        for product_off_allergen in product_off_allergens:
            # In OFF, allergens sont sous la forme "en:gluten"
            # import pdb; pdb.set_trace()
            matches = re.search(":([a-zA-Z]+)", product_off_allergen)
            if matches and matches.group(1):
                # We get the allergen name
                # try to find allergen in database fitting ignoring letter case
                TODO
                allergen_find = allergens_obj.search([('name', '=', matches.group(1))])
                print("youîiiiiiiiiiiiiiiii")
        # set many to many

    @api.multi
    def button_fill_product_informations(self):
        for product in self:
            off_product = self._get_product_in_off_database()

    @api.multi
    def button_get_allergens_off(self):
        for product in self:
            off_product = self._get_product_in_off_database()
            product._set_product_allergens(off_product)
            # login_session_object = openfoodfacts.utils.login_into_OFF()
            # allergens = openfoodfacts.facets.get_allergens()

# openfoodfacts.products.get_by_facets({'trace': 'egg','country': 'france'})

# res = openfoodfacts.products.get_product("8019428000105")
# openfoodfacts.products.advanced_search({"search_terms":"lait d'avoine the bridge"})
#
# res['product']
# res['product']['nutriscore_grade']
# # donne une lettre a b c d e
# res['product']['allergens_tags']
# # donne ['en:gluten']
