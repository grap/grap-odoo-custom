from operator import itemgetter

from odoo import _, api, models


class ReportBomAllergens(models.AbstractModel):
    _name = "report.mrp_bom_print.report_bom_allergens"
    _description = "BoM Allergens report"

    # In case allergen's code is not set, and user wants to print with code
    _DEFAULT_ALLERGENE_CODE = "XX"
    _NO_CATEGORY_STRING = _("Others")

    @api.model
    def _get_report_values(self, docids, data=None):
        allergen_obj = self.env["product.allergen"]
        allergens_all = allergen_obj.search([])

        docargs = {
            "allergens": allergens_all,
            "default_allergen_code": self._DEFAULT_ALLERGENE_CODE,
            "boms_and_allergens": self._prepare_data(data),
        }
        return docargs

    @api.model
    def _prepare_data(self, data):
        line_obj = self.env["bom.print.wizard.line"]
        allergen_obj = self.env["product.allergen"]
        allergens_all = allergen_obj.search([])

        # Preparing data for report → list of list
        # Goal : list of [meal_categ, product_name, allergen1, allergen2..]
        # ordered by meal categories. allergenX is '✔️' or ''
        # 1st step : Get line by line and create list
        boms = line_obj.browse([int(x) for x in data["line_data"]])
        boms_and_allergens = []
        for bom in boms:
            tmpList_allergens = []
            # Category
            if bom.bom_id.meal_category_id:
                tmpList_allergens.append(bom.bom_id.meal_category_id.name)
            else:
                tmpList_allergens.append(self._NO_CATEGORY_STRING)
            # Product name
            tmpList_allergens.append(bom.bom_id.product_id.name)
            # Allergens
            for allergen in allergens_all:
                if allergen.id in bom.bom_id.bom_allergen_ids.ids:
                    tmpList_allergens.append("✔️")
                else:
                    tmpList_allergens.append(" ")
            boms_and_allergens.append(tmpList_allergens)

        # 2nd step : Sort by category
        # example : [['categ1', 'product1', 'x', '', 'x'],
        #            ['categ1', 'product2', '', 'x', 'x'],
        #            ['categ2', 'product2', '', 'x', 'x']]
        boms_and_allergens.sort(key=itemgetter(0))
        return boms_and_allergens
