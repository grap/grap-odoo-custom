Customize Odoo / odoo / `product` module.

- Set default `list` view for product, and not `kanban` (save planet and
  ressources). (A product image is one server call)
- Refactor `product.product` and `product.template` list views.
- Change decimal precisions.
  - `product.decimal_stock_weight`: 2 -\> 3
  - `product.decimal_volume`: 2 -\> 3
  - `product.decimal_product_uom`: 2 -\> 3

- Model `product.product` and `product.template`:
  - set `standard_price` as copiable, when product are duplicated.
  - track `standard_price` and sale prices fields.
