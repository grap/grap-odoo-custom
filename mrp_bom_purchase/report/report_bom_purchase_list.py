from operator import itemgetter

from odoo import api, models


class ReportBomPurchaseList(models.AbstractModel):
    _name = "report.mrp_bom_purchase.report_bom_purchase_list"
    _description = "BoM Purchase list"

    @api.model
    def _get_report_values(self, docids, data=None):
        data_purchase, data_produce = self._prepare_data_to_purchase_and_produce(data)
        docargs = {
            "manufacture_list": self._prepare_data_to_manufacture(data),
            "purchase_list": data_purchase,
            "produce_list": data_produce,
            "purchase_total_cost": self._prepare_total_cost(data),
            "currency_symbol": self._prepare_currency(data),
        }
        return docargs

    @api.model
    def calculate_qty_for_one_product(
        self, bom_line_product_qty, bom_qty, desired_qty, digits
    ):
        _bom_qty = max(1, bom_qty)
        return round(bom_line_product_qty * desired_qty / _bom_qty, digits)

    # Returns two lists purchase_list, produce_list
    # INTERMEDIATES PRODUCTS to produce_list = [bom_id1, bom_id2]
    # COMPONENTS PRODUCTS to purchase_list = [
    #       ['category', 'product_name', quantity, uom, price_unit, subtotal], ... ]
    @api.model
    def _prepare_data_to_purchase_and_produce(self, data):
        bom_line_obj = self.env["mrp.bom.line"]

        # Get the selected BoMs and their associated lines
        wiz_boms_lines = self.env["bom.print.purchase.list.wizard.line"].browse(
            data["line_data"]
        )
        bom_lines_by_product = {}
        produce_list = {}
        for wiz_bom_line in wiz_boms_lines:
            bom = wiz_bom_line.bom_id
            bom_qty = bom.product_qty
            # Search bomlines without bomlines of notes or sections
            bom_lines = bom_line_obj.search(
                [("bom_id", "=", bom.id), ("product_id", "!=", False)]
            )
            for bom_line in bom_lines:
                product = bom_line.product_id
                product_id = product.id
                # Check if product has a nested BoM and get the FIRST ONE
                if product.bom_ids:
                    nested_bom = product.bom_ids[0]
                    nested_bom_lines = bom_line_obj.search(
                        [("bom_id", "=", nested_bom.id), ("product_id", "!=", False)]
                    )
                    # Add its bom lines them to the set of bom_lines..
                    bom_lines += nested_bom_lines
                    # And remove intermediate product from it as it will be in produce_list
                    bom_lines = bom_lines.filtered(lambda line: line != bom_line)

                    # INTERMEDIATE PRODUCT TO PRODUCE
                    # Calculate values of this line
                    produce_product_qty = bom_line.product_qty
                    produce_subtotal = (
                        bom_line.product_qty * bom_line.standard_price_unit
                    )
                    # Add quantity if product is already there
                    if product_id in produce_list:
                        produce_list[product_id]["to_produce_quantity"] = round(
                            produce_list[product_id]["to_produce_quantity"]
                            + produce_product_qty,
                            3,
                        )
                        produce_list[product_id]["to_produce_subtotal"] = round(
                            produce_list[product_id]["to_produce_subtotal"]
                            + produce_subtotal,
                            3,
                        )
                    else:
                        produce_list[product_id] = {
                            "to_produce_product_name": bom_line.product_id.name.capitalize(),
                            "to_produce_quantity": round(produce_product_qty, 3),
                            "to_produce_uom": bom_line.product_uom_id.name,
                            "to_produce_price_unit": bom_line.standard_price_unit,
                            "to_produce_subtotal": round(produce_subtotal, 2),
                        }

            # COMPONENTS PRODUCTS to purchase_list
            for bom_line in bom_lines:
                product_id = bom_line.product_id.id
                product_qty = self.calculate_qty_for_one_product(
                    bom_line.product_qty, bom_qty, wiz_bom_line.quantity, 3
                )
                bom_line_subtotal = round(product_qty * bom_line.standard_price_unit, 2)
                # Add quantity if product is already there
                if product_id in bom_lines_by_product:
                    bom_lines_by_product[product_id]["quantity"] = round(
                        bom_lines_by_product[product_id]["quantity"] + product_qty, 3
                    )
                    bom_lines_by_product[product_id]["subtotal"] = round(
                        bom_lines_by_product[product_id]["subtotal"]
                        + bom_line_subtotal,
                        3,
                    )
                else:
                    bom_lines_by_product[product_id] = {
                        "category": bom_line.product_id.categ_id.complete_name,
                        "product_name": bom_line.product_id.name.capitalize(),
                        "quantity": round(product_qty, 3),
                        "uom": bom_line.product_uom_id.name,
                        "price_unit": round(bom_line.standard_price_unit, 3),
                        "subtotal": round(bom_line_subtotal, 3),
                    }

        # Formate purchase_list dict in list the way we want
        purchase_list = []
        for bom_line in bom_lines_by_product.values():
            purchase_list.append(
                [
                    bom_line[field]
                    for field in [
                        "category",
                        "product_name",
                        "quantity",
                        "uom",
                        "price_unit",
                        "subtotal",
                    ]
                ]
            )
        # Sort the purchase list by product name and, optionally, category
        purchase_list.sort(
            key=itemgetter(1, 0)
            if data["option_group_by_product_category"]
            else itemgetter(1)
        )

        # Formate produce_list dict in list the way we want
        produce_list_clean = []
        for bom in produce_list.values():
            produce_list_clean.append(
                [
                    bom[field]
                    for field in [
                        "to_produce_product_name",
                        "to_produce_quantity",
                        "to_produce_uom",
                        "to_produce_price_unit",
                        "to_produce_subtotal",
                    ]
                ]
            )

        return purchase_list, produce_list_clean

    @api.model
    def _prepare_data_to_manufacture(self, data):
        line_obj = self.env["bom.print.purchase.list.wizard.line"]

        # Preparing data for report → dict of list
        # It looks like this
        # { wiz_bom_id1 : [bom1_name, qty, uom],
        #   wiz_bom_id2: [bom2_name, qty, uom]
        # }
        wiz_boms_lines = line_obj.browse([int(x) for x in data["line_data"]])
        manufacture_list = []
        for wiz_bom_line in wiz_boms_lines:
            manufacture_list.append(
                [
                    wiz_bom_line.bom_id.display_name,
                    round(wiz_bom_line.quantity, 3),
                    wiz_bom_line.bom_uom_id.name,
                    round(wiz_bom_line.bom_id.standard_price_total, 3),
                    round(wiz_bom_line.wizard_line_subtotal, 3),
                ]
            )
        return manufacture_list

    @api.model
    def _prepare_total_cost(self, data):
        line_obj = self.env["bom.print.purchase.list.wizard.line"]
        wiz_boms_lines = line_obj.browse([int(x) for x in data["line_data"]])
        return round(sum(wiz_boms_lines.mapped("wizard_line_subtotal")), 3)

    @api.model
    def _prepare_currency(self, data):
        line_obj = self.env["bom.print.purchase.list.wizard.line"]
        wiz_boms_lines = line_obj.browse([int(x) for x in data["line_data"]])
        return wiz_boms_lines[0].currency_id.symbol if wiz_boms_lines else ""
