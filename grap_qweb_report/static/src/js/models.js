/*
Copyright (C) 2018-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

odoo.define('grap_qweb_report.models', function (require) {
    'use strict';

    var models = require('point_of_sale.models');

    var order_super = models.Order.prototype;

    models.load_fields("res.company", ['siret']);

    models.Order = models.Order.extend({

        /**
        * * Detailed values for tax lines.
        * @returns {dict} List of taxes description.
        */
        get_tax_details_with_base: function () {
            var self = this;
            var tax_dict = {};
            var result = [];
            this.orderlines.each(function (line) {
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
                var tax_name = String(key) + '%';
                var tax_name_with_underscore = tax_name + ' ' + Array(10 - tax_name.length).join('_');
                result.push({
                    'name': tax_name,
                    'tax_name_with_underscore': tax_name_with_underscore,
                    'base': value.tax_base,
                    'amount': value.tax_amount,
                });
            });
            return result;
        },

        export_for_printing: function () {
            var res = order_super.export_for_printing.apply(this, arguments);
            res.pricelist_id = this.pricelist.id;
            res.pricelist_name = this.pricelist.name;
            res.pricelist_default =
                res.pricelist_id === this.pos.config.pricelist_id[0];
            res.tax_details_with_base = this.get_tax_details_with_base();

            return res;
        },

    });
});
