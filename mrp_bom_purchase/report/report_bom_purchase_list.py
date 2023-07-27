from operator import itemgetter

from odoo import api, models


class ReportBomPurchaseList(models.AbstractModel):
    _name = "report.mrp_bom_purchase.report_bom_purchase_list"
    _description = "BoM Purchase list"

    @api.model
    def _get_report_values(self, docids, data=None):
        data_purchase, data_produce = self._prepare_data_to_purchase_and_produce(data)
        manufacture_bom_list = self._prepare_data_to_manufacture(data)
        docargs = {
            "manufacture_bom_list": manufacture_bom_list,
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
    # Intermediates products to PRODUCE_LIST = [bom_id1, bom_id2]
    # Components products to PURCHASE_LIST = [
    #       ['category', 'product_name', quantity, uom, price_unit, subtotal], ... ]
    @api.model
    def _prepare_data_to_purchase_and_produce(self, data):
        bom_line_obj = self.env["mrp.bom.line"]

        # Get the selected BoMs and their associated lines
        wiz_boms_lines = self.env["bom.print.purchase.list.wizard.line"].browse(
            data["line_data"]
        )

        purchase_list = {}
        produce_list = {}
        for wiz_bom_line in wiz_boms_lines:
            bom = wiz_bom_line.bom_id
            bom_qty = bom.product_qty
            # Search bomlines without bomlines of notes or sections
            bom_lines = bom_line_obj.search(
                [("bom_id", "=", bom.id), ("product_id", "!=", False)]
            )
            # bom_lines_with_factor = [[bom_lines1, factor1],[bom_lines2, factor2],...]
            bom_lines_with_factor = []
            # Nested BoMs
            # Add BoM product to PRODUCE_LIST and their bom lines for PURCHASE_LIST
            for bom_line in bom_lines:
                product = bom_line.product_id
                product_id = product.id
                # /!\ Limitation : only get the first nested BoM
                if product.bom_ids:
                    nested_bom = product.bom_ids[0]
                    nested_bom_lines = bom_line_obj.search(
                        [("bom_id", "=", nested_bom.id), ("product_id", "!=", False)]
                    )
                    # PURCHASE_LIST
                    # Add nested bom lines with factor which is
                    # bom_line parent quantity divided by nested bom quantity
                    parent_bom_factor_qty = (
                        bom_line.product_qty / nested_bom.product_qty
                    )
                    bom_lines_with_factor.append(
                        [nested_bom_lines, parent_bom_factor_qty]
                    )
                    # And remove this intermediate product which will be in PRODUCE_LIST
                    bom_lines = bom_lines.filtered(lambda line: line != bom_line)

                    # PRODUCE_LIST
                    # Add intermediate product
                    # Calculate values of this line
                    produce_product_qty = self.calculate_qty_for_one_product(
                        bom_line.product_qty, bom_qty, wiz_bom_line.quantity, 3
                    )
                    produce_subtotal = round(
                        produce_product_qty * bom_line.standard_price_unit, 3
                    )

                    # Add product or just quantity if product is already there
                    if product_id in produce_list:
                        produce_list[product_id][
                            "to_produce_product_in_bom_name"
                        ] += str(
                            ", "
                            + wiz_bom_line.bom_id.display_name
                            + " x"
                            + str(produce_product_qty)
                        )
                        produce_list[product_id]["to_produce_quantity"] = round(
                            produce_list[product_id]["to_produce_quantity"]
                            + produce_product_qty,
                            4,
                        )
                        produce_list[product_id]["to_produce_subtotal"] = round(
                            produce_list[product_id]["to_produce_subtotal"]
                            + produce_subtotal,
                            3,
                        )
                    else:
                        produce_list[product_id] = {
                            "to_produce_product_name": bom_line.product_id.name.capitalize(),
                            "to_produce_product_in_bom_name": wiz_bom_line.bom_id.display_name
                            + " x"
                            + str(produce_product_qty),
                            "to_produce_quantity": round(produce_product_qty, 3),
                            "to_produce_uom": bom_line.product_uom_id.name,
                            "to_produce_price_unit": bom_line.standard_price_unit,
                            "to_produce_subtotal": round(produce_subtotal, 3),
                        }

            # PURCHASE_LIST
            # Components products to PURCHASE_LIST
            # Formate bom_lines to be add with nested bom lines, factor is 1
            bom_lines_with_factor.append([bom_lines, 1])

            # Nested BoMs Lines
            for bom_lines_with_quantity in bom_lines_with_factor:
                parent_bom_factor_qty = bom_lines_with_quantity[1]
                for bom_line in bom_lines_with_quantity[0]:
                    product_id = bom_line.product_id.id
                    product_qty = self.calculate_qty_for_one_product(
                        bom_line.product_qty,
                        bom_qty,
                        wiz_bom_line.quantity * parent_bom_factor_qty,
                        3,
                    )
                    bom_line_subtotal = round(
                        product_qty * bom_line.standard_price_unit, 3
                    )
                    # Add quantity if product is already there
                    if product_id in purchase_list:
                        purchase_list[product_id]["quantity"] = round(
                            purchase_list[product_id]["quantity"] + product_qty, 3
                        )
                        purchase_list[product_id]["subtotal"] = round(
                            purchase_list[product_id]["subtotal"] + bom_line_subtotal,
                            3,
                        )
                    else:
                        purchase_list[product_id] = {
                            "category": bom_line.product_id.categ_id.complete_name,
                            "product_name": bom_line.product_id.name.capitalize(),
                            "quantity": round(product_qty, 3),
                            "uom": bom_line.product_uom_id.name,
                            "price_unit": round(bom_line.standard_price_unit, 3),
                            "subtotal": round(bom_line_subtotal, 3),
                        }

        # Formate purchase_list dict in list the way we want
        purchase_list_clean = []
        for bom_line in purchase_list.values():
            purchase_list_clean.append(
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
        # Sort the PURCHASE_LIST by product name and, optionally, category
        purchase_list_clean.sort(
            key=itemgetter(0, 1)
            if data["option_group_by_product_category"]
            else itemgetter(1)
        )

        # Formate PRODUCE_LIST dict in list the way we want
        produce_list_clean = []
        for bom in produce_list.values():
            produce_list_clean.append(
                [
                    bom[field]
                    for field in [
                        "to_produce_product_name",
                        "to_produce_product_in_bom_name",
                        "to_produce_quantity",
                        "to_produce_uom",
                        "to_produce_price_unit",
                        "to_produce_subtotal",
                    ]
                ]
            )

        return purchase_list_clean, produce_list_clean

    @api.model
    def _prepare_data_to_manufacture(self, data):
        line_obj = self.env["bom.print.purchase.list.wizard.line"]
        bom_line_obj = self.env["mrp.bom.line"]
        wiz_boms = line_obj.browse([int(x) for x in data["line_data"]])

        # Get all BOM lines without bomlines of notes or sections
        bom_lines = bom_line_obj.search(
            [
                ("bom_id", "in", wiz_boms.mapped("bom_id").ids),
                ("product_id", "!=", False),
            ]
        )

        manufacture_bom_list = []
        for wiz_bom in wiz_boms:
            bom = wiz_bom.bom_id
            bom_qty = bom.product_qty
            desired_bom_qty = wiz_bom.quantity

            filtered_bom_lines = bom_lines.filtered(lambda line: line.bom_id == bom)

            tmp_bom_lines = []
            for bom_line in filtered_bom_lines:
                product_qty = self.calculate_qty_for_one_product(
                    bom_line.product_qty, bom_qty, desired_bom_qty, 3
                )
                tmp_bom_lines.append(
                    [
                        bom_line.product_id.display_name,
                        product_qty,
                        bom_line.product_uom_id.name,
                    ]
                )

            manufacture_bom_list.append(
                [
                    bom.display_name,
                    desired_bom_qty,
                    wiz_bom.bom_uom_id.name,
                    round(wiz_bom.bom_id.standard_price_total, 3),
                    round(wiz_bom.wizard_line_subtotal, 3),
                    tmp_bom_lines,
                    bom.description_short,
                    bom.description_long,
                    bom.description_packaging,
                ]
            )
        # manufacture_bom_list = [['SEITAN_BOM', 2.0, 'Unit(s)', 55.0, 110.0,
        #   [['Carrots', 10.0, 'kg'], ['Onions', 4.0, 'Unit(s)']]] , bom2]
        return manufacture_bom_list

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
