from operator import itemgetter

from odoo import api, models


class ReportBomPurchaseList(models.AbstractModel):
    _name = "report.mrp_bom_purchase.report_bom_purchase_list"
    _description = "BoM Purchase list"

    @api.model
    def _get_report_values(self, docids, data=None):
        docargs = {
            "purchase_list": self._prepare_data(data),
            "purchase_total_cost": self._prepare_total_cost(data),
            "currency_symbol": self._prepare_currency(data),
        }
        return docargs

    @api.model
    def calculate_qty_for_one_product(
        self, bom_line_product_qty, bom_qty, desired_qty, digits
    ):
        _bom_qty = 1 if bom_qty == 0 else bom_qty
        return round(bom_line_product_qty * desired_qty / _bom_qty, digits)

    @api.model
    def _prepare_data(self, data):
        line_obj = self.env["bom.print.purchase.list.wizard.line"]
        bom_line_obj = self.env["mrp.bom.line"]

        # Preparing data for report → dict of list
        # It looks like this
        # { product_id1: [categ1, product_name1, qty1, uom1, price_unit1, subtotal1],
        #   product2: [categ2, product_name2, qty2, uom1, price_unit2, subtotal2]
        # }
        wiz_boms_lines = line_obj.browse([int(x) for x in data["line_data"]])
        purchase_list = {}
        for wiz_bom_line in wiz_boms_lines:
            # Get bom_lines of selected BoM
            bom = wiz_bom_line.bom_id
            bom_id = bom.id
            bomlines = bom_line_obj.search([("bom_id.id", "=", bom_id)])

            # Add entry in dictionnary for each new product or add quantity
            for bomline in bomlines:
                if bomline.product_id.id in purchase_list.keys():
                    qty = purchase_list[bomline.product_id.id][
                        2
                    ] + self.calculate_qty_for_one_product(
                        bomline.product_qty, bom.product_qty, wiz_bom_line.quantity, 3
                    )
                else:
                    qty = self.calculate_qty_for_one_product(
                        bomline.product_qty, bom.product_qty, wiz_bom_line.quantity, 3
                    )
                subtotal = round(qty * bomline.standard_price_unit, 2)
                purchase_list[bomline.product_id.id] = [
                    bomline.product_id.categ_id.complete_name,
                    bomline.product_id.name.title(),
                    round(qty, 3),
                    bomline.product_uom_id.name,
                    bomline.standard_price_unit,
                    subtotal,
                ]

        # Clean it for printing PDF datas
        # Step 1 : remove product_id keys
        purchaseList_cleaned = []
        for pl_line in purchase_list:
            purchaseList_cleaned.append(purchase_list.get(pl_line))

        # import pdb; pdb.set_trace()
        # Step 2 : Sort by alphabetical order or/then category
        if data["option_group_by_product_category"]:
            purchaseList_cleaned.sort(key=itemgetter(0, 1))
        else:
            purchaseList_cleaned.sort(key=itemgetter(1))

        return purchaseList_cleaned

    @api.model
    def _prepare_total_cost(self, data):
        line_obj = self.env["bom.print.purchase.list.wizard.line"]
        wiz_boms_lines = line_obj.browse([int(x) for x in data["line_data"]])
        return sum(
            wiz_boms_line["wizard_line_subtotal"] for wiz_boms_line in wiz_boms_lines
        )

    @api.model
    def _prepare_currency(self, data):
        line_obj = self.env["bom.print.purchase.list.wizard.line"]
        wiz_boms_lines = line_obj.browse([int(x) for x in data["line_data"]])
        currency_symbol = (
            wiz_boms_lines[0].currency_id.symbol if len(wiz_boms_lines) > 0 else ""
        )
        return currency_symbol
