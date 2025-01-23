import copy

from odoo import api, models


class ReportBomWizardProduction(models.AbstractModel):
    _name = "report.mrp_bom_wizard_production.report_bom_wizard_production"
    _description = "BoM Wizard Production"

    # data are given by bom_wizard_production.py
    @api.model
    def _get_report_values(self, docids, data=None):
        (
            data_manufacture_list,
            data_manufacture_total_cost,
            data_purchase_list,
            data_intermediate_product_list,
            data_matrix_boms,
            data_matrix_product_bom,
        ) = self._prepare_data_to_purchase_and_produce(data)
        purchase_total_cost = round(sum(map(lambda x: x[5], data_purchase_list)), 2)
        docargs = {
            "manufacture_bom_list": data_manufacture_list,
            "manufacture_total_cost": data_manufacture_total_cost,
            "intermediate_product_list": data_intermediate_product_list,
            "purchase_list": data_purchase_list,
            "purchase_total_cost": purchase_total_cost,
            "data_matrix_boms": data_matrix_boms,
            "data_matrix_product_bom": data_matrix_product_bom,
            "currency_symbol": data["currency_symbol"],
            "wizard_lines": self._get_wizard_lines(data),
        }
        return docargs

    @api.model
    def calculate_qty_for_one_product(
        self, bom_line_product_qty, bom_qty, desired_qty, digits
    ):
        _bom_qty = max(1, bom_qty)
        return round(bom_line_product_qty * desired_qty / _bom_qty, digits)

    @api.model
    def _get_wizard_lines(self, data):
        return self.env["bom.wizard.production.line"].browse(data["line_data"])

    # Used in _prepare_data_to_purchase_and_produce
    @api.model
    def create_data_purchase_list_and_pre_data_matrix_product_bom(
        self,
        line_template,
        bom_lines_with_factor,
        purchase_list,
        pre_data_matrix_product_bom,
        wiz_line,
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
                    wiz_line.quantity * parent_bom_factor_qty,
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
                    bom_id_concerned = wiz_line.bom_id.id

                if product_id not in pre_data_matrix_product_bom:
                    # add template : set 0 for each futur BoM column
                    pre_data_matrix_product_bom[product_id] = copy.deepcopy(
                        line_template
                    )
                    pre_data_matrix_product_bom[product_id][bom_id_concerned][
                        1
                    ] = round(product_qty, 3)
                    pre_data_matrix_product_bom[product_id][
                        "product_name"
                    ] = product.name
                    pre_data_matrix_product_bom[product_id]["uom"] = str(
                        bom_line.product_uom_id.name
                    )
                else:
                    rounded_sum = round(
                        pre_data_matrix_product_bom[product_id][bom_id_concerned][1]
                        + product_qty,
                        3,
                    )
                    pre_data_matrix_product_bom[product_id][bom_id_concerned][
                        1
                    ] = rounded_sum

        return purchase_list, pre_data_matrix_product_bom

    @api.model
    def create_datas_from_nested_boms(self, data_intermediate_product_list, wiz_line):
        """
        This function is called in a loop with all BoMs of Wizard
        It gradually fills data_intermediate_product_list with quantities

        :param data_intermediate_product_list: array being filled gradually
        :param wiz_line: bom.wizard.production.line with Bom, Bom Qty, Desired Qty
        :return: data_intermediate_product_list, bom_lines_with_factor (?)
        """
        bom_lines_with_factor = []

        # Loop in every bom_line of the BoM
        for bom_line in wiz_line.bom_id.bom_line_ids:
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

                # data_purchase_list :
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

                # data_intermediate_product_list
                # Add intermediate product and calculate values of this line
                produce_product_qty = self.calculate_qty_for_one_product(
                    bom_line.product_qty,
                    wiz_line.bom_id.product_qty,
                    wiz_line.quantity,
                    3,
                )
                produce_subtotal = round(
                    produce_product_qty * bom_line.standard_price_unit, 3
                )

                to_produce_product_bom_name = (
                    wiz_line.bom_id.display_name + " x" + str(produce_product_qty)
                )
                # Add product or just quantity if product is already there
                if product_id in data_intermediate_product_list:
                    data_intermediate_product_list[product_id][
                        "to_produce_product_bom_name"
                    ] += str(", " + to_produce_product_bom_name)
                    data_intermediate_product_list[product_id][
                        "to_produce_quantity"
                    ] = round(
                        data_intermediate_product_list[product_id][
                            "to_produce_quantity"
                        ]
                        + produce_product_qty,
                        4,
                    )
                    data_intermediate_product_list[product_id][
                        "to_produce_subtotal"
                    ] = round(
                        data_intermediate_product_list[product_id][
                            "to_produce_subtotal"
                        ]
                        + produce_subtotal,
                        3,
                    )
                else:
                    _product_name = bom_line.product_id.name.capitalize()
                    data_intermediate_product_list[product_id] = {
                        "to_produce_product_name": _product_name,
                        "to_produce_product_bom_name": to_produce_product_bom_name,
                        "to_produce_quantity": round(produce_product_qty, 3),
                        "to_produce_uom": bom_line.product_uom_id.name,
                        "to_produce_price_unit": bom_line.standard_price_unit,
                        "to_produce_subtotal": round(produce_subtotal, 3),
                    }

        return (
            data_intermediate_product_list,
            bom_lines_with_factor,
        )

    @api.model
    def _prepare_data_to_purchase_and_produce(self, data):
        """
        This function formate datas for the production report
        It has two main loops.
        First to get all BoMs and nested BoMs
        Second to set datas

        :param: data: datas from wizard
        :return: lists and data for report
            - data_manufacture_list
            - data_manufacture_total_cost
            - data_purchase_list
            - data_intermediate_product_list
            - data_matrix_boms : used in matrix head table
            - data_matrix_product_bom
        """

        # Init obj and variables
        mrp_bom_line_obj = self.env["mrp.bom.line"]
        wiz_lines = self._get_wizard_lines(data)
        data_manufacture_list = []
        pre_data_intermediate_product_list = {}
        pre_data_purchase_list = {}
        pre_data_matrix_product_bom = {}
        line_template = {}
        pre_data_matrix_boms = {}

        # ==== SET data_manufacture_total_cost
        data_manufacture_total_cost = round(
            sum(wiz_lines.mapped("wizard_line_subtotal")), 3
        )

        # First loop of wizard lines (BoM) :
        #   - create line_template with BoM and nested BoM for data_matrix_product_bom
        #   - set data_manufacture_list
        # line_template has as many zero as Bom, it looks like :
        # {10: [BomName1, 0], 5: [BomName2, 0]}
        line_template = {}
        pre_data_matrix_boms = {}
        for wiz_line in wiz_lines:
            bom = wiz_line.bom_id
            bom_id = bom.id
            desired_bom_qty = wiz_line.quantity

            # Add bom to line_template
            line_template[bom_id] = [bom.display_name, 0]

            # ==== SET data_manufacture_list
            data_manufacture_list.append(
                [
                    bom.display_name,
                    bom.description_packaging,
                    desired_bom_qty,
                    wiz_line.bom_uom_id.name,
                    round(wiz_line.bom_id.standard_price, 3),
                    round(wiz_line.wizard_line_subtotal, 3),
                ]
            )

            # ==== First step for data_matrix_boms
            # Array of BoM and their quantities being added iteratively
            if not pre_data_matrix_boms.get(bom.id):
                pre_data_matrix_boms[bom_id] = [
                    bom.display_name,
                    round(wiz_line.quantity, 3),
                    wiz_line.bom_uom_id.name,
                ]
            else:
                rounded_sum = round(
                    pre_data_matrix_boms[bom_id][1] + wiz_line.quantity, 3
                )
                pre_data_matrix_boms[bom_id][1] = rounded_sum

            bom_lines = mrp_bom_line_obj.search(
                [("bom_id", "=", bom_id), ("product_id", "!=", False)]
            )
            # ==== Second step for data_matrix_boms : adding nested BoMs
            for bom_line in bom_lines:
                if bom_line.product_id.bom_ids:
                    # /!\ Limitation : Search its bomlines and get the FIRST nested BoM
                    nested_bom = bom_line.product_id.bom_ids[0]
                    nested_bom_id = nested_bom.id

                    # Add nested bom to line_template and pre_data_matrix_boms
                    line_template[nested_bom_id] = [nested_bom.display_name, 0]
                    quantity_with_factor = bom_line.product_qty * wiz_line.quantity
                    if not pre_data_matrix_boms.get(nested_bom_id):
                        pre_data_matrix_boms[nested_bom_id] = [
                            "↳ " + nested_bom.display_name,
                            round(quantity_with_factor, 3),
                            bom_line.product_uom_id.name,
                        ]
                    else:
                        rounded_sum = round(
                            pre_data_matrix_boms[nested_bom_id][1]
                            + quantity_with_factor,
                            3,
                        )
                        pre_data_matrix_boms[nested_bom_id][1] = rounded_sum

        # ==== SET data_matrix_boms with right format for PD
        data_matrix_boms = []
        for value in pre_data_matrix_boms.values():
            data_matrix_boms.append(value[0] + " - " + str(value[1]) + " " + value[2])

        # Second loop of wizard lines (this loop uses line_template set previously)
        for wiz_line in wiz_lines:
            bom = wiz_line.bom_id
            bom_qty = bom.product_qty
            # Search bomlines except notes and sections
            bom_lines = mrp_bom_line_obj.search(
                [("bom_id", "=", bom.id), ("product_id", "!=", False)]
            )

            # create_datas_from_nested_boms :
            #  - start to set data_intermediate_product_list
            #  - get all bom_lines_with_factor*
            # *factor indicate qty from parent BoM that will by apply to children
            # *factor should not to be confused with product_qty of mrp.bom.lin
            (
                pre_data_intermediate_product_list,
                bom_lines_with_factor,
            ) = self.create_datas_from_nested_boms(
                pre_data_intermediate_product_list, wiz_line
            )

            # Add parent bom_lines
            bom_lines_with_factor.append([bom_lines, 1, False])
            # Example :
            # [[mrp.bom.line(10, 11), 2.0, mrp.bom(5,)], [mrp.bom.line(8,), 1, False]]
            # mrp_bom_line id8 has a BoM with two mrp_bom_line id10 and id11

            # Go through concatenation of nested BoMs Lines and Boms Lines
            (
                pre_data_purchase_list,
                pre_data_matrix_product_bom,
            ) = self.create_data_purchase_list_and_pre_data_matrix_product_bom(
                line_template,
                bom_lines_with_factor,
                pre_data_purchase_list,
                pre_data_matrix_product_bom,
                wiz_line,
                bom_qty,
            )

        # ==== SET data_matrix_product_bom
        data_matrix_product_bom = []
        for value in pre_data_matrix_product_bom.values():
            row = [value["product_name"] + " (" + value["uom"] + ")"]
            for _key, _value in value.items():
                if _key not in ("product_name", "uom"):
                    row.append(_value[1])
            data_matrix_product_bom.append(row)

        data_matrix_product_bom = [
            [val if val != 0 else " " for val in sublist]
            for sublist in data_matrix_product_bom
        ]

        # ==== SET data_purchase_list
        data_purchase_list = []
        for bom_line in pre_data_purchase_list.values():
            data_purchase_list.append(
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
        # Sort the purchase_list by product name and optionally category
        if data["option_group_by_product_category"]:
            data_purchase_list.sort(key=lambda x: (x[0], x[1]))
        else:
            data_purchase_list.sort(key=lambda x: x[1])

        # ==== SET data_intermediate_product_lis
        data_intermediate_product_list = []
        for bom in pre_data_intermediate_product_list.values():
            data_intermediate_product_list.append(
                [
                    bom[field]
                    for field in [
                        "to_produce_product_name",
                        "to_produce_product_bom_name",
                        "to_produce_quantity",
                        "to_produce_uom",
                        "to_produce_price_unit",
                        "to_produce_subtotal",
                    ]
                ]
            )

        return (
            data_manufacture_list,
            data_manufacture_total_cost,
            data_purchase_list,
            data_intermediate_product_list,
            data_matrix_boms,
            data_matrix_product_bom,
        )
