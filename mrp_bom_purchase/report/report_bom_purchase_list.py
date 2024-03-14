import copy
from operator import itemgetter

from odoo import api, models


class ReportBomPurchaseList(models.AbstractModel):
    _name = "report.mrp_bom_purchase.report_bom_purchase_list"
    _description = "BoM Purchase list"

    @api.model
    def _get_report_values(self, docids, data=None):
        (
            data_purchase,
            data_produce,
            data_all_bom,
            data_list_matrix_product_bom,
        ) = self._prepare_data_to_purchase_and_produce(data)
        purchase_total_cost = round(sum(map(lambda x: x[5], data_purchase)), 2)
        manufacture_bom_list = self._prepare_data_to_manufacture(data)
        docargs = {
            "manufacture_bom_list": manufacture_bom_list,
            "purchase_list": data_purchase,
            "produce_list": data_produce,
            "manufacture_total_cost": self._prepare_manufacture_total_cost(data),
            "purchase_total_cost": purchase_total_cost,
            "data_all_bom": data_all_bom,
            "data_list_matrix_product_bom": data_list_matrix_product_bom,
            "currency_symbol": self._prepare_currency(data),
        }
        return docargs

    @api.model
    def calculate_qty_for_one_product(
        self, bom_line_product_qty, bom_qty, desired_qty, digits
    ):
        _bom_qty = max(1, bom_qty)
        return round(bom_line_product_qty * desired_qty / _bom_qty, digits)

    #  Used in _prepare_data_to_purchase_and_produce
    @api.model
    def create_data_purchase_and_data_product_bom_qty(
        self,
        line_template,
        bom_lines_with_factor,
        purchase_list,
        data_product_bom_qty,
        wiz_bom_line,
        bom_qty,
    ):
        # Go through concatenation of nested BoMs Lines and Boms Lines
        for bom_lines_with_quantity in bom_lines_with_factor:
            parent_bom_factor_qty = bom_lines_with_quantity[1]
            for bom_line in bom_lines_with_quantity[0]:
                product = bom_line.product_id
                product_id = product.id
                product_qty = self.calculate_qty_for_one_product(
                    bom_line.product_qty,
                    bom_qty,
                    wiz_bom_line.quantity * parent_bom_factor_qty,
                    3,
                )
                bom_line_subtotal = round(product_qty * bom_line.standard_price_unit, 3)
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

                if bom_lines_with_quantity[2] is not False:
                    # nested bom_line → choose nested_bom
                    bom_id_concerned = bom_lines_with_quantity[2].id
                else:
                    bom_id_concerned = wiz_bom_line.bom_id.id
                if product_id not in data_product_bom_qty:
                    # add template : set 0 for each futur BoM column
                    data_product_bom_qty[product_id] = copy.deepcopy(line_template)
                    data_product_bom_qty[product_id][bom_id_concerned][1] = round(
                        product_qty, 3
                    )
                    data_product_bom_qty[product_id]["product_name"] = product.name
                    data_product_bom_qty[product_id]["uom"] = str(
                        bom_line.product_uom_id.name
                    )
                else:
                    rounded_sum = round(
                        data_product_bom_qty[product_id][bom_id_concerned][1]
                        + product_qty,
                        3,
                    )
                    data_product_bom_qty[product_id][bom_id_concerned][1] = rounded_sum

        return purchase_list, data_product_bom_qty

    #  Used in _prepare_data_to_purchase_and_produce
    @api.model
    def create_data_produce(self, data_produce, wiz_bom_line, bom_lines, bom_qty):
        bom_lines_with_factor = []

        for bom_line in bom_lines:
            product = bom_line.product_id
            product_id = product.id
            # /!\ Limitation : only get the first nested BoM
            # Each nested BoM (intermediate product) is a product to produce
            if product.bom_ids:
                nested_bom = product.bom_ids[0]

                # Search bom_lines
                nested_bom_lines = self.env["mrp.bom.line"].search(
                    [("bom_id", "=", nested_bom.id), ("product_id", "!=", False)]
                )

                # DATA_PURCHASE :
                #   - fill bom_lines_with_factor
                #   - filter bom_lines to remove INTERMEDIATE product
                # Add nested bom lines with factor which is
                # bom_line parent quantity divided by nested bom quantity
                parent_bom_factor_qty = (
                    bom_line.product_qty / nested_bom.product_qty
                    if nested_bom.product_qty != 0
                    else 1
                )
                # Create this list that will be used for other data*
                bom_lines_with_factor.append(
                    [nested_bom_lines, parent_bom_factor_qty, nested_bom]
                )

                # DATA_PRODUCE
                # Add intermediate product and calculate values of this line
                produce_product_qty = self.calculate_qty_for_one_product(
                    bom_line.product_qty, bom_qty, wiz_bom_line.quantity, 3
                )
                produce_subtotal = round(
                    produce_product_qty * bom_line.standard_price_unit, 3
                )
                # Add product or just quantity if product is already there
                if product_id in data_produce:
                    data_produce[product_id]["to_produce_product_in_bom_name"] += str(
                        ", "
                        + wiz_bom_line.bom_id.display_name
                        + " x"
                        + str(produce_product_qty)
                    )
                    data_produce[product_id]["to_produce_quantity"] = round(
                        data_produce[product_id]["to_produce_quantity"]
                        + produce_product_qty,
                        4,
                    )
                    data_produce[product_id]["to_produce_subtotal"] = round(
                        data_produce[product_id]["to_produce_subtotal"]
                        + produce_subtotal,
                        3,
                    )
                else:
                    data_produce[product_id] = {
                        "to_produce_product_name": bom_line.product_id.name.capitalize(),
                        "to_produce_product_in_bom_name": wiz_bom_line.bom_id.display_name
                        + " x"
                        + str(produce_product_qty),
                        "to_produce_quantity": round(produce_product_qty, 3),
                        "to_produce_uom": bom_line.product_uom_id.name,
                        "to_produce_price_unit": bom_line.standard_price_unit,
                        "to_produce_subtotal": round(produce_subtotal, 3),
                    }
        return data_produce, bom_lines_with_factor

    # Returns four lists :
    # 1. DATA_PURCHASE : component products that we'll be purchased
    #   → [['category', 'product_name', quantity, uom, price_unit, subtotal], ... ]
    # 2. DATA_PRODUCE : intermediates products that we'll be produced [bom_id1, bom_id2]
    # 3. DATA_ALL_BOM : all boms :
    #   → [['Tomato pie', 0.1, 'kg'], ['Wood Panel', 1.0, 'Unit(s)']]
    # 4. DATA_LIST_MATRIX_PRODUCT_BOM
    #   → [['Pie', 1.0, ' '], ['Tomatoes', 0.5, ' '], ..]
    @api.model
    def _prepare_data_to_purchase_and_produce(self, data):
        mrp_bom_line_obj = self.env["mrp.bom.line"]
        # Get the selected BoMs and their associated lines
        wiz_boms_lines = self.env["bom.print.purchase.list.wizard.line"].browse(
            data["line_data"]
        )
        wiz_boms_lines.mapped("bom_id")

        # ==== LINE_TEMPLATE and DATA_ALL_BOM
        # Create template with as many zero as BoM to prepare data_list_matrix_product_bom
        # Look like : {10: [BomName1, 0], 5: [BomName2, 0]}
        # Need to go through nested boms one first time
        line_template = {}
        pre_data_all_bom = {}
        for wiz_bom_line in wiz_boms_lines:
            bom = wiz_bom_line.bom_id
            bom_id = bom.id

            # Add bom to line_template
            line_template[bom_id] = [bom.display_name, 0]

            # ==== DATA_ALL_BOM
            if not pre_data_all_bom.get(bom.id):
                pre_data_all_bom[bom_id] = [
                    bom.display_name,
                    round(wiz_bom_line.quantity, 3),
                    wiz_bom_line.bom_uom_id.name,
                ]
            else:
                rounded_sum = round(
                    pre_data_all_bom[bom_id][1] + wiz_bom_line.quantity, 3
                )
                pre_data_all_bom[bom_id][1] = rounded_sum

            # /!\ Limitation : Search its bomlines and get the FIRST nested BoM
            bom_lines = mrp_bom_line_obj.search(
                [("bom_id", "=", bom_id), ("product_id", "!=", False)]
            )
            for bom_line in bom_lines:
                if bom_line.product_id.bom_ids:
                    nested_bom = bom_line.product_id.bom_ids[0]
                    nested_bom_id = nested_bom.id

                    # Add nested bom to line_template
                    line_template[nested_bom_id] = [nested_bom.display_name, 0]
                    # DATA_ALL_BOM
                    quantity_with_factor = bom_line.product_qty * wiz_bom_line.quantity
                    if not pre_data_all_bom.get(nested_bom_id):
                        pre_data_all_bom[nested_bom_id] = [
                            "↳ " + nested_bom.display_name,
                            round(quantity_with_factor, 3),
                            bom_line.product_uom_id.name,
                        ]
                    else:
                        rounded_sum = round(
                            pre_data_all_bom[nested_bom_id][1] + quantity_with_factor, 3
                        )
                        pre_data_all_bom[nested_bom_id][1] = rounded_sum

        # ==== DATA_ALL_BOM : formate for PDF
        data_all_bom = []
        for value in pre_data_all_bom.values():
            data_all_bom.append(value[0] + " - " + str(value[1]) + " " + value[2])

        # ==== Init variables
        pre_data_produce = {}
        pre_data_purchase = {}
        data_product_bom_qty = {}

        # ==== Create pre_DATA_PRODUCE, pre_DATA_PURCHASE and pre_DATA_LIST_MATRIX_PRODUCT_BOM
        for wiz_bom_line in wiz_boms_lines:
            bom = wiz_bom_line.bom_id
            bom_qty = bom.product_qty
            # Search bomlines without bomlines of notes or sections
            bom_lines = mrp_bom_line_obj.search(
                [("bom_id", "=", bom.id), ("product_id", "!=", False)]
            )
            # ==== DATA_PROCUCE (coming from nested boms)
            # Also add their bom lines in bom_lines_with_factor to create DATA_PURCHASE
            pre_data_produce, bom_lines_with_factor = self.create_data_produce(
                pre_data_produce, wiz_bom_line, bom_lines, bom_qty
            )
            # bom_lines_with_factor = [[bom_lines1, factor1, nested_bom_lines1], ..]

            # ==== DATA_PURCHASE (components products)
            # ==== and DATA_LIST_MATRIX_PRODUCT_BOM
            # Formate bom_lines to be add with nested bom lines, factor is 1
            bom_lines_with_factor.append([bom_lines, 1, False])

            # # Go through concatenation of nested BoMs Lines and Boms Lines
            (
                pre_data_purchase,
                data_product_bom_qty,
            ) = self.create_data_purchase_and_data_product_bom_qty(
                line_template,
                bom_lines_with_factor,
                pre_data_purchase,
                data_product_bom_qty,
                wiz_bom_line,
                bom_qty,
            )

        # ==== Precreate DATA_LIST_MATRIX_PRODUCT_BOM
        data_list_matrix_product_bom = []
        for value in data_product_bom_qty.values():
            row = [value["product_name"] + " (" + value["uom"] + ")"]
            for _key, _value in value.items():
                if _key not in ("product_name", "uom"):
                    row.append(_value[1])
            data_list_matrix_product_bom.append(row)

        data_list_matrix_product_bom = [
            [val if val != 0 else " " for val in sublist]
            for sublist in data_list_matrix_product_bom
        ]

        # Formate purchase_list dict in list the way we want
        data_purchase = []
        for bom_line in pre_data_purchase.values():
            data_purchase.append(
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
        data_purchase.sort(
            key=itemgetter(0, 1)
            if data["option_group_by_product_category"]
            else itemgetter(1)
        )

        # ==== DATA_PRODUCE : formate dict in list the way we want
        data_produce = []
        for bom in pre_data_produce.values():
            data_produce.append(
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

        return data_purchase, data_produce, data_all_bom, data_list_matrix_product_bom

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
                    bom.notes,
                    bom.description_packaging,
                ]
            )
        # manufacture_bom_list = [['SEITAN_BOM', 2.0, 'Unit(s)', 55.0, 110.0,
        #   [['Carrots', 10.0, 'kg'], ['Onions', 4.0, 'Unit(s)']]] , bom2]
        return manufacture_bom_list

    @api.model
    def _prepare_manufacture_total_cost(self, data):
        line_obj = self.env["bom.print.purchase.list.wizard.line"]
        wiz_boms_lines = line_obj.browse([int(x) for x in data["line_data"]])
        return round(sum(wiz_boms_lines.mapped("wizard_line_subtotal")), 3)

    @api.model
    def _prepare_currency(self, data):
        line_obj = self.env["bom.print.purchase.list.wizard.line"]
        wiz_boms_lines = line_obj.browse([int(x) for x in data["line_data"]])
        return wiz_boms_lines[0].currency_id.symbol if wiz_boms_lines else ""
