Customize Odoo / odoo / `product` module.

- Set default `list` view for product, and not `kanban` (save planet and
  ressources). (A product image is one server call)
- Refactor `product.product` and `product.template` list views.
- Change decimal precisions.
  - `product.decimal_stock_weight`: 2 -\> 3
  - `product.decimal_cost_price`: 2 -\> 3
- Model `product.product`: set `standard_price` as copiable, when
  product are duplicated.
