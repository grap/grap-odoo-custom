from odoo import _, models


class PurchaseOrderXlsx(models.AbstractModel):
    _name = "report.report_xlsx.purchase_order_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def _define_custom_formats(self, workbook, orders):
        currency = orders[0].currency_id
        s_before = currency.symbol if currency.position == "before" else ""
        s_after = " %s" % currency.symbol if currency.position == "after" else ""
        currency_format = (
            f"{f'{s_before}'}#,##0.{'0' * currency.decimal_places}{f'{s_after}'}"
        )
        self.format_currency_right = workbook.add_format(
            {"align": "right", "num_format": currency_format}
        )

    def generate_xlsx_report(self, workbook, data, orders):
        self._define_formats(workbook)
        self._define_custom_formats(workbook, orders)
        ws_params = self._get_ws_params(workbook, data, orders.mapped("order_line"))[0]

        for order in orders:
            ws_name = order.name
            ws_name = self._check_ws_name(ws_name)
            ws = workbook.add_worksheet(ws_name)
            generate_ws_method = getattr(self, ws_params["generate_ws_method"])
            generate_ws_method(workbook, ws, ws_params, data, order.order_line)

    def _get_columns_spec(self, order_lines):
        supplierinfo_render = (
            "order_line.product_id"
            "._get_supplierinfo_from_purchase_order_line(order_line)"
        )

        res = [
            {
                "name": "product_code",
                "header_name": _("product Code"),
                "data": self._render(f"{supplierinfo_render}.product_code or ''"),
                "width": 20,
            },
            {
                "name": "product_name",
                "header_name": _("Product Name"),
                "data": self._render(f"{supplierinfo_render}.product_name or ''"),
                "width": 20,
            },
            {
                "name": "name",
                "header_name": _("Description"),
                "data": self._render("order_line.name"),
                "width": 20,
            },
            {
                "name": "product_qty",
                "header_name": _("Quantity"),
                "data": self._render("order_line.product_qty"),
                "width": 10,
            },
            {
                "name": "product_uom",
                "header_name": _("Unit"),
                "data": self._render("order_line.product_uom.name"),
                "width": 10,
            },
            {
                "name": "price_unit",
                "header_name": _("Unit Price"),
                "data": self._render("order_line.price_unit"),
                "format": self.format_currency_right,
                "width": 10,
            },
        ]
        for i, field in enumerate(["discount", "discount2", "discount3"]):
            if any(order_lines.mapped(field)):
                res.append(
                    {
                        "name": field,
                        "header_name": _("Discount %s %%" % (i + 1)),
                        "data": self._render(f"order_line.{field} /  100"),
                        "format": self.format_tcell_percent_right,
                        "width": 15,
                    }
                )
        res += [
            {
                "name": "price_subtotal",
                "header_name": _("Price Subtotal VAT Excl."),
                "data": self._render("order_line.price_subtotal"),
                "format": self.format_currency_right,
                "width": 20,
            }
        ]

        return res

    def _get_ws_params(self, wb, data, order_lines):
        columns_spec = self._get_columns_spec(order_lines)

        order_line_template = {}
        for spec in columns_spec:
            order_line_template[spec["name"]] = {
                "header": {
                    "value": spec["header_name"],
                },
                "data": {
                    "value": spec["data"],
                    "format": spec.get("format", False),
                },
                "width": spec["width"],
            }

        return [
            {
                "generate_ws_method": "_purchase_order_report",
                "wanted_list": [x["name"] for x in columns_spec],
                "col_specs": order_line_template,
            }
        ]

    def _purchase_order_report(self, workbook, ws, ws_params, data, order_lines):

        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers["standard"])
        ws.set_footer(self.xls_footers["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        # row_pos = self._write_ws_title(ws, row_pos, ws_params)
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_yellow_left,
        )
        ws.freeze_panes(row_pos, 0)

        for order_line in order_lines:
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="data",
                render_space={
                    "order_line": order_line,
                },
                default_format=self.format_tcell_left,
            )
