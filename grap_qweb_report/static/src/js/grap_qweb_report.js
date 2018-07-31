/*
Copyright (C) 2018-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

"use strict";

openerp.grap_qweb_report = function (instance) {
    var module = instance.point_of_sale;
    var round_pr = instance.web.round_precision

    /* 
        Overwrite : Order getTaxDetails function to return
        detailed values for tax lines.
    */
    module.Order = module.Order.extend({
        getTaxDetails: function(){
            var self = this;
            var tax_dict = {};
            var result = [];
            this.get('orderLines').each(function(line){
                var line_detail = line.get_all_prices();
                for(var id in line_detail.taxDetails){
                    var tax = self.pos.taxes_by_id[id];
                    if (tax.amount in tax_dict){
                        tax_dict[tax.amount]['tax_amount'] += line_detail.tax;
                        tax_dict[tax.amount]['tax_base'] += line_detail.priceWithoutTax;

                    } else {
                        tax_dict[tax.amount] = {
                            'tax_amount': line_detail.tax,
                            'tax_base': line_detail.priceWithoutTax,
                        };
                    }
                }
            });
            $.each(tax_dict, function( key, value ) {
                var tax_name = _t('VAT ') + 100 * key + '%';
                tax_name += ' ' + Array(14 - tax_name.length).join('_');
                result.push({
                    'tax_amount': value['tax_amount'],
                    'tax_base': value['tax_base'],
                    'tax_name': tax_name,
                })
            });
            return result;
        },
    });

};
