Customize Odoo / odoo / `point_of_sale` module.

- Display for members of `point_of_sale.group_pos_user` the following
  menu entries:
  - "Point Of Sale \> Analysis"
  - "Point Of Sale \> Configuration"
  - "Point Of Sale \> Orders \> Sessions"
- Allow non admin user to create `pos.category` elements.
- Default accounting journal is the same for pos orders and invoices.
- Set 'Update quantities in stock' field of PoS config as 'Real Time',
  by default.
- Add 'Available in PoS' field in the `product.template` tree view.
- Hide some fields (`user_id`, `pos_reference`) by default in the `pos.order`
  tree view, to make the view lighter.

Customize `point_of_sale` Front End.

- Make bigger the button to reset the search input field.

Customize `product_template`.

- Field `availaible_in_pos` default True except in Joint Buying context
