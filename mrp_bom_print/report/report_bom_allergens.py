from odoo import api, models


class ReportBomAllergens(models.AbstractModel):
    _name = "report.mrp_bom_print.report_bom_allergens"
    _description = "BoM Allergens report"

    # in case code is not ste in allergen and user print report with code
    _DEFAULT_ALLERGENE_CODE = "XX"

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
        boms = line_obj.browse([int(x) for x in data["line_data"]])
        boms_and_allergens = []
        for bom in boms:
            tmpList_allergens = []
            tmpList_allergens.append(bom.bom_id.product_id.name)
            for allergen in allergens_all:
                if allergen.id in bom.bom_id.bom_allergen_ids.ids:
                    # we found this allergen
                    tmpList_allergens.append("✔️")
                else:
                    tmpList_allergens.append(" ")
            boms_and_allergens.append(tmpList_allergens)

        return boms_and_allergens
