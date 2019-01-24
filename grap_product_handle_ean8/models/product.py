# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, exceptions, models
from openerp.addons.barcodes.barcodes import barcode_nomenclature


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Accept ean13 and ean8 barcodes
    # need to use old api for constraints but ready for new API
    @api.multi
    @api.constrains('ean13')
    def _check_ean_key(self):
        res = True
        for product in self.filtered(lambda x: x.ean13):
            my_model = self.env['barcode.nomenclature']
            if len(product['ean13']) == 8:
                res = my_model.check_encoding(product['ean13'], 'ean8')
            elif len(product['ean13']) == 13:
                res = my_model.check_encoding(product['ean13'], 'ean13')
            else:
                raise exceptions.ValidationError('Le code barre doit être \
                    composé de 8 ou 13 chiffres')
        return res

    _constraints = [(_check_ean_key, 'Code barre incorrecte', ['ean13'])]
