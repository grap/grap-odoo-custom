/*
Copyright (C) 2018-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/


openerp.grap_qweb_report = function (instance) {
    'use strict';

    var module = instance.point_of_sale;
    var _t = instance.web._t;

    var moduleOrderParent = module.Order;

    module.Order = module.Order.extend({

        /**
        * Overwrite : Order getTaxDetails function to return
        * detailed values for tax lines.
        * @returns {dict} List of taxes description.
        */
        getTaxDetails: function () {
            var self = this;
            var tax_dict = {};
            var result = [];
            this.get('orderLines').each(function (line) {
                var line_detail = line.get_all_prices();
                for (var id in line_detail.taxDetails) {
                    var tax = self.pos.taxes_by_id[id];
                    if (tax.amount in tax_dict) {
                        tax_dict[tax.amount].tax_amount += line_detail.tax;
                        tax_dict[tax.amount].tax_base +=
                            line_detail.priceWithoutTax;

                    } else {
                        tax_dict[tax.amount] = {
                            'tax_amount': line_detail.tax,
                            'tax_base': line_detail.priceWithoutTax,
                        };
                    }
                }
            });
            $.each(tax_dict, function (key, value) {
                var tax_name = _t('VAT ') + String(100 * key) + '%';
                tax_name += ' ' + Array(14 - tax_name.length).join('_');
                result.push({
                    'name': tax_name,
                    'base': value.tax_base,
                    'amount': value.tax_amount,
                });
            });
            return result;
        },

        export_for_printing: function(attributes){
            var order = moduleOrderParent.prototype.export_for_printing.apply(this, arguments);
            var partner = this.get_client();
            if (partner && partner.property_product_pricelist) {
                order.pricelist_id = partner.property_product_pricelist[0];
                order.pricelist_name = partner.property_product_pricelist[1];
            } else {
                order.pricelist_id = this.pos.config.pricelist_id[0];
                order.pricelist_name = this.pos.config.pricelist_id[1];
            }
            order.pricelist_default = order.pricelist_id === this.pos.config.pricelist_id[0];
            return order;
        },

    });

};
