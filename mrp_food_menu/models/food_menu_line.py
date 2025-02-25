# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FoodMenuLine(models.Model):
    _name = "mrp.food.menu.line"
    _description = "Food Menu Line"

    _sql_constraints = [
        (
            "menu_required_fields_product_qty",
            "CHECK(display_type IS NOT NULL OR"
            "(product_id IS NOT NULL AND product_uom_qty IS NOT NULL))",
            "Missing required fields on menu line : product and quantity.",
        ),
        (
            "non_menu_null_fields",
            "CHECK(display_type IS NULL OR"
            "(product_id IS NULL AND product_uom_qty = 1))",
            "Forbidden values on note and section menu line",
        ),
    ]

    menu_id = fields.Many2one(
        comodel_name="mrp.food.menu",
        required=True,
    )
    sequence = fields.Integer(default=10)

    # Fields to handle section & note
    name = fields.Text(string="Description")

    # Order-related fields
    company_id = fields.Many2one(
        related="menu_id.company_id",
    )

    # Fields specifying custom line logic
    display_type = fields.Selection(
        [("line_section", "Section"), ("line_note", "Note")],
        default=False,
        help="Technical field for UX purpose.",
    )

    product_id = fields.Many2one(
        comodel_name="product.product",
    )

    product_uom_qty = fields.Float(
        string="Quantity",
        digits="Product Unit of Measure",
        default=1.0,
        required=True,
    )

    product_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Unit of Measure",
        related="product_id.uom_id",
    )

    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        domain="""[
        '&',
            '|',
                ('company_id', '=', False),
                ('company_id', '=', company_id),
            '&',
                '|',
                    ('product_id','=',product_id),
                    '&',
                        ('product_tmpl_id.product_variant_ids','=',product_id),
                        ('product_id','=',False),
        ('type', '=', 'normal')]""",
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        for menu_line in self.filtered(lambda x: x.product_id.bom_count != 0):
            menu_line.bom_id = menu_line.product_id.bom_ids[0]
