# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_PRODUCT_CODE_GENERIC_TLA = "XXX"


class ProductProduct(models.Model):
    _inherit = "product.product"

    tla = fields.Char(
        string="Trigram",
        size=3,
        copy=False,
        help="A three-letter acronym (TLA), or three-letter abbreviation,"
        " is an abbreviation consisting of three letters.",
    )

    tla_to_change = fields.Boolean(
        default=True,
    )

    # [DEPRECATED] Commentaire juste après plus valide car TLA pas généré automatiquement.
    #  Par contre, une contrainte est bien faite dans le onchange qui vérifie l'unicité
    #
    # Ce code levera une merde si dans des données de démo ya plusieurs produits au nom
    # court qui se ressemble et génère un truc générique qui va alors crée 2 tla
    # similaires. ex :
    # - produit "Ab" → tla = AXX
    # - produit "Abc" → tla = ABC
    # - produit "Abd" → tla = ABD
    # - produit "Abdc" → tla = AXX (car ABD et ABC pris)
    # Et donc là deux AXX ça marche pas
    # Cas particulier : on s'en fout ou bien sinon pas une sql constrains mais
    # une ValidationError par l'interface sur la fonction inverse ?
    # _sql_constraints = [
    #     ("unique_tla", "unique(tla)", "Trigram should be unique"),
    # ]

    # ========== Others
    meal_category_id = fields.Many2one(
        comodel_name="mrp.meal.category",
        string="Meal category",
    )

    # Methods
    @api.onchange("tla")
    def check_tla_change(self):
        if self.tla is not False:
            self.tla = self.tla.upper()
            if (
                self.env["product.product"].search_count(
                    [
                        ("tla", "=", self.tla),
                    ]
                )
                > 0
            ):
                res0 = self.env["product.product"].search([("tla", "=", self.tla)])[0]
                if res0.id != self._origin.id:
                    raise ValidationError(
                        _("Trigram already used by an other product : %s.") % res0.name
                    )

    # J'aurais aimé que ça soit un truc automatique qui dépend du nom mais :
    # - ça fait une quadrature du cercle : on le met en compute pour qu'il soit calculé
    # en fonction du nom, mais en le mettant en compute, il est recalculé
    # quand on va le chercher pour le bom. Et au recalcul, il va choisir un autre tla
    # vu que l'algo est fait pour ça. Et je peux pas dire, re-calcule pas si yen a déjà un
    # vu que le but est de le changer si on change le nom
    # p-e u'il me manque une pièce au puzzle : est-ce qu'avec un compute, on peut
    # quand même dire d'aller chercher en base à certains moments ?
    # - ça sera très long à l'installation sur grosse base. C'est p-e mieux que ça
    # soit pas généré automatiquement mais que pour les produits avec BoM
    # @api.depends("display_name")
    @api.multi
    def generate_tla(self):
        tmp_created_onfly_tla = []  # for first compute during module installation
        for product in self.filtered(lambda x: x.name):
            # Simpligy name : keep only alphanumeric
            simple_name = re.sub(r"[^A-Za-z0-9]+", "", product.name)
            if 1 <= len(simple_name) <= 2:
                product.tla = _PRODUCT_CODE_GENERIC_TLA
                product.tla_to_change = True
            else:
                product.tla_to_change = False
                # Takes 0-1-2 product's name letters
                new_tla_start = simple_name[0:2].upper()
                new_tla_end = simple_name[2].upper()
                new_tla = new_tla_start + new_tla_end
                i = 2
                # Loop until finding new product TLA, changing last TLA letter
                while (
                    product.env["product.product"].search_count(
                        [
                            ("tla", "=", new_tla),
                        ]
                    )
                    > 0
                    or tmp_created_onfly_tla.count(new_tla) > 0
                ):
                    # End ot the product's name → Add generic letters and break
                    if i + 1 >= len(simple_name):
                        new_tla = new_tla_start[0:1] + _PRODUCT_CODE_GENERIC_TLA[0:2]
                        product.tla_to_change = True
                        break
                    # Next letter is space, but it's not the end of the name
                    if simple_name[i + 1] == " ":
                        i += 1
                        continue
                    # Loop with next letter
                    else:
                        new_tla_end = simple_name[i + 1].upper()
                        new_tla = new_tla_start + new_tla_end
                        i += 1
                tmp_created_onfly_tla.append(new_tla)
                product.tla = new_tla
