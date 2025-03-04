# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    """
    Note 1 : j'ai hesité à enlever la route si pas de BoM mais effet de bord :
    Si tu coches "Manufacture" et que tu as pas de BoM encore, ça le décoche. Donc naze.
    """

    def _compute_bom_count(self):
        super()._compute_bom_count()
        manufacture_route = self.env.ref("mrp.route_warehouse0_manufacture").id
        for product in self.filtered(lambda x: x.bom_count != 0):
            product.route_ids = [
                (4, manufacture_route),
            ]
        return True
