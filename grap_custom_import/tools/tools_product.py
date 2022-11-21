# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _

from .tools_generic import _str_monetary_to_float, _str_percent_to_float, _str_to_float


def _handle_product_name(self, vals):
    """
    - Sanitize the product name
    - search if product still exist and raise an error if yes
    """
    ProductProduct = self.env["product.product"]
    res = vals.copy()
    name = res.get("name", False)
    # TODO don't hardcode '*'
    # get the value from the ir.config.parameter.
    name = name.replace("*", "")
    name = name.strip()
    products = ProductProduct.search([("name", "=", name)])
    if products:
        raise Exception(
            _("The following item(s) still exist %s")
            % ",".join(products.mapped("name"))
        )
    res["name"] = name
    return res


def handle_supplier_info_values(self, vals):
    res = vals.copy()
    ResPartner = self.env["res.partner"]
    if not vals["grap_import_supplier_name"]:
        return res
    partners = ResPartner.search([("name", "=", vals["grap_import_supplier_name"])])
    if len(partners) == 0:
        raise Exception(
            _("The supplier '%s' has not been found.")
            % vals["grap_import_supplier_name"]
        )
    elif len(partners) >= 2:
        raise Exception(
            _("%d suppliers found for '%s'.")
            % (len(partners), vals["grap_import_supplier_name"])
        )
    seller_vals = {
        "name": partners[0].id,
        "price": _str_monetary_to_float(res["grap_import_supplier_gross_price"]),
        "discount": _str_percent_to_float(res["grap_import_supplier_discount_1"] * 100),
        "discount2": _str_percent_to_float(
            res["grap_import_supplier_discount_2"] * 100
        ),
        "product_code": res["grap_import_supplier_product_code"],
        "product_name": res["grap_import_supplier_product_name"],
        "package_qty": _str_to_float(res["grap_import_supplier_uom_packaging_qty"]),
    }
    res["seller_ids"] = [(0, False, seller_vals)]

    return res


def _handle_label_ids(self, vals):
    """Convert 3 columns (label_1 / label_2 / label_3)
    into a list of label_ids
    """
    res = vals.copy()
    ProductLabel = self.env["product.label"]
    label_values = [
        res.get("grap_import_label_1", False),
        res.get("grap_import_label_2", False),
        res.get("grap_import_label_3", False),
    ]
    label_values = list(filter(lambda a: a, label_values))
    res["label_ids"] = []
    for label_value in label_values:
        label = ProductLabel.search(
            ["|", ("code", "=", label_value), ("name", "=", label_value)]
        )
        if not label:
            raise Exception(_("Incorrect label value %s") % label_value)
        res["label_ids"].append(label.id)
    return res


def _guess_extra_values(self, vals):
    """Guess extra values, based on existing ones"""
    res = vals.copy()
    # product_values['to_weight'] = (product.uom_id == uom_kilo.id)
    return res
