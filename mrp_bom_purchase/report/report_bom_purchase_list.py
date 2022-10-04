from operator import itemgetter

from odoo import api, models


class ReportBomPurchaseList(models.AbstractModel):
    _name = "report.mrp_bom_purchase.report_bom_purchase_list"
    _description = "BoM Purchase list"

    @api.model
    def _get_report_values(self, docids, data=None):
        docargs = {
            "purchase_list": self._prepare_data(data),
        }
        return docargs

    @api.model
    def _prepare_data(self, data):
        line_obj = self.env["bom.print.purchase.list.wizard.line"]
        bom_line_obj = self.env["mrp.bom.line"]

        # Preparing data for report → dict of list
        # It looks like this
        # {product_id1: [categ1, p  roduct_name1, qty1, uom1],
        # product2: [categ2, product_name2, qty2, uom1]}
        boms = line_obj.browse([int(x) for x in data["line_data"]])
        purchase_list = {}
        for bom in boms:
            # Get bom_lines of selected BoM
            bom_id = bom.bom_id.id
            bomlines = bom_line_obj.search([("bom_id.id", "=", bom_id)])

            # Add entry in dictionnary for each product or add quantity
            for bomline in bomlines:
                if bomline.product_id.id in purchase_list.keys():
                    qty = purchase_list[bomline.product_id.id][2] + bomline.product_qty
                else:
                    qty = bomline.product_qty
                purchase_list[bomline.product_id.id] = [
                    bomline.product_id.categ_id.complete_name,
                    bomline.product_id.name,
                    qty,
                    bomline.product_uom_id.name,
                ]
                # example : [['categ1', 'product1', 'qty', 'uom'],
                #            ['categ1', 'product2', 'qty', 'uom'],
                #            ['categ2', 'product3', 'qty', 'uom']]

        # Clean it for printing PDF datas
        # Step 1 : remove product_id keys
        purchaseList_cleaned = []
        for pl_line in purchase_list:
            purchaseList_cleaned.append(purchase_list.get(pl_line))

        if data["option_group_by_product_category"]:
            # Step 2 : Sort by category
            # example : [['categ1', 'product1', 'qty', 'uom'],
            #            ['categ1', 'product2', 'qty', 'uom'],
            #            ['categ2', 'product3', 'qty', 'uom']]
            purchaseList_cleaned.sort(key=itemgetter(0))
        return purchaseList_cleaned
