# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo import _, api, models
from odoo.exceptions import UserError


class ProductReplenish(models.TransientModel):
    _inherit = "product.replenish"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if "route_ids" in fields and res.get("product_id"):
            if res.get("warehouse_id"):
                warehouse = self.env["stock.warehouse"].browse(res["warehouse_id"])
            else:
                warehouse = self.env["stock.warehouse"].search(
                    [("company_id", "=", self.env.company.id)], limit=1
                )

            product = self.env["product.product"].browse(res["product_id"])
            rule = self.env["procurement.group"]._get_rule(
                product, warehouse.lot_stock_id, {}
            )

            if rule and rule.route_id:
                res["route_ids"] = [(6, 0, [rule.route_id.id])]

        return res

    # Override Odoo function, based on v18 code, to get notification after Replenish
    def launch_replenishment(self):
        now = datetime.now()
        uom_reference = self.product_id.uom_id
        self.quantity = self.product_uom_id._compute_quantity(
            self.quantity, uom_reference, rounding_method="HALF-UP"
        )
        try:
            self.env["procurement.group"].with_context(**self.env.context).run(
                [
                    self.env["procurement.group"].Procurement(
                        self.product_id,
                        self.quantity,
                        uom_reference,
                        self.warehouse_id.lot_stock_id,  # Location
                        _("Manual Replenishment"),  # Name
                        _("Manual Replenishment"),  # Origin
                        self.warehouse_id.company_id,
                        self._prepare_run_values(),  # Values
                    )
                ]
            )

        except UserError as error:
            raise UserError(error) from error

        notification = self._get_replenishment_order_notification(now)
        # Close Wizard Replenish
        act_window_close = {
            "type": "ir.actions.act_window_close",
            "infos": {"done": True},
        }
        if notification:
            notification["params"]["next"] = act_window_close
        return notification

    # Handling Buy and Manufacture action
    def _get_replenishment_order_notification(self, date):
        route_action = self.route_ids.mapped("rule_ids.action")
        replenish = False

        if "buy" in route_action:
            # self.env['purchase.order.line'].flush_model()
            model = "purchase.order"
            actn = self.env.ref("purchase.action_rfq_form")
            title = _("Product was added to this draft Purchase Order.")
            # Replenish can complete a existing PO that why we search on PO lines
            replenish = (
                self.env["purchase.order.line"]
                .search([("write_date", ">=", date)], limit=1)
                .order_id
            )
            label = replenish.name + " - " + replenish.partner_id.name

        elif "manufacture" in route_action:
            # self.env['mrp.production'].flush_model()
            model = "mrp.production"
            actn = self.env.ref("mrp.action_mrp_production_form")
            title = _("Product was added to this Manufacturing Order.")
            replenish = self.env["mrp.production"].search(
                [("write_date", ">=", date)], limit=1
            )
            label = replenish.name

        if replenish is not False:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("%s", title),
                    "message": "%s",
                    "links": [
                        {
                            "label": label,
                            "url": f"#action={actn.id}&id={replenish.id}&model{model}",
                        }
                    ],
                    "sticky": True,
                },
            }
        return False
