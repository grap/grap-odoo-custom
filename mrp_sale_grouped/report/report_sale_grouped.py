# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class ReportSaleGrouped(models.AbstractModel):
    _name = "report.mrp_sale_grouped.report_sale_grouped"
    _description = "Report for Grouped Sale and Production"

    @api.model
    def _get_report_values(self, docids, data=None):
        (
            all_sale_order,
            list_sale_order_product_quantity,
        ) = self._prepare_data_to_matrix_customer_product(data)
        docargs = {
            "all_sale_order": all_sale_order,
            "list_sale_order_product_quantity": list_sale_order_product_quantity,
        }
        return docargs

    @api.model
    def calculate_qty_for_one_product(
        self, bom_line_product_qty, bom_qty, desired_qty, digits
    ):
        _bom_qty = max(1, bom_qty)
        return round(bom_line_product_qty * desired_qty / _bom_qty, digits)

    # Data is sale.order ids
    # First returns list sale_order for head of PDF table
    # Second return dict of product__id and quantities sort by sale_order
    @api.model
    def _prepare_data_to_matrix_customer_product(self, data):
        all_sale_order_ids = data["line_data"]
        all_sale_order = self.env["sale.order"].search(
            [("id", "in", all_sale_order_ids)]
        )
        sale_order_lines = self.env["sale.order.line"].search(
            [("order_id", "in", all_sale_order_ids)]
        )

        all_products = sale_order_lines.mapped("product_id")
        all_products_ids = all_products.ids
        product_names = (
            self.env["product.product"].browse(all_products_ids).mapped("name")
        )

        all_customers = sale_order_lines.mapped("order_partner_id")
        len(all_customers)

        # Create template with zero to be prepare to matrix product / sale_order
        line_template = {}
        for order_id in all_sale_order_ids:
            line_template[order_id] = 0
        line_template["subtotal"] = 0
        line_template["uom"] = ""

        dict_sale_order_prod_qty = {}
        # Browse each sale_order
        for order in all_sale_order:
            # Browse each sale_order_line
            for line in order.order_line:
                product = line.product_id
                # Get quantity with product uom (convert if uom of sale_order_line is different)
                quantity = line.product_uom._compute_quantity(
                    line.product_uom_qty,
                    line.product_id.uom_id,
                    rounding_method="HALF-UP",
                )
                if product.id not in dict_sale_order_prod_qty:
                    # if not dict_sale_order_prod_qty.get(product.id):
                    # New product → new line that we fill with zero
                    dict_sale_order_prod_qty[product.id] = line_template.copy()
                    dict_sale_order_prod_qty[product.id][order.id] = quantity
                    dict_sale_order_prod_qty[product.id]["subtotal"] = quantity
                    dict_sale_order_prod_qty[product.id][
                        "uom"
                    ] = line.product_id.uom_id.name
                else:
                    # Product already created, add quantity to the right colmun
                    dict_sale_order_prod_qty[product.id][order.id] += quantity
                    dict_sale_order_prod_qty[product.id]["subtotal"] += quantity

        # Converting the dict into an array of arrays
        # Get : {10: {22: 24.0, 16: 0, 'subtotal': 24.0, 'uom': 'Unit(s)'},
        #        28: {22: 0, 16: 3.0, 'subtotal': 3.0, 'uom': 'Unit(s)'},}
        # Convert into : [['Customizable Desk', 24.0, ' ', '24.0 Unit(s)'],
        #                ['Acoustic Bloc Screens', ' ', 3.0, '3.0 Unit(s)'], ]
        list_sale_order_product_quantity = [
            [product_names[i]]
            + list(dict_sale_order_prod_qty[all_products_ids[i]].values())
            for i in range(len(all_products_ids))
        ]
        # Replace 0 by blank
        list_sale_order_product_quantity = [
            [val if val != 0 else " " for val in sublist]
            for sublist in list_sale_order_product_quantity
        ]
        # Join last two elements for UoM text in PDF
        list_sale_order_product_quantity = [
            sublist[:-2] + [" ".join(map(str, sublist[-2:]))]
            for sublist in list_sale_order_product_quantity
        ]

        # Return all customers and prepared lines
        return all_sale_order, list_sale_order_product_quantity
