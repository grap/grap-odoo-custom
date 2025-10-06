/*
Copyright (C) 2018-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

odoo.define('fermente_report_pos.OrderReceipt', function (require) {
    'use strict';

    const {Order} = require("point_of_sale.models");
    const Registries = require("point_of_sale.Registries");

    const OverloadOrder = (OriginalOrder) =>
        class extends OriginalOrder {

            export_for_printing() {
                var receipt = super.export_for_printing(...arguments);
                receipt.pricelist_id = this.pricelist.id;
                receipt.pricelist_name = this.pricelist.name;
                receipt.pricelist_default =
                    receipt.pricelist_id === this.pos.config.pricelist_id[0];
                return receipt;
            }
        };

    Registries.Model.extend(Order, OverloadOrder);

    return Order;

});
