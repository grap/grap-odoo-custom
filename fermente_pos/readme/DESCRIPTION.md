Customize Odoo / odoo / `point_of_sale` module.

- Display for members of `point_of_sale.group_pos_user` the following
  menu entries:
  - "Point Of Sale \> Analysis"
  - "Point Of Sale \> Configuration"
- Allow non admin user to create `pos.category` elements.
- Default accounting journal is the same for pos orders and invoices.
- Set 'Update quantities in stock' field of PoS config as 'Real Time',
  by default.
- Add 'Available in PoS' field in the `product.template` tree view.
- Add a lot of missing field on the simple pos.config form view.
- Allow admin user to create new pos.config, via kanban view.
- Allow non admin user to edit receipt header and footer.

Customize `point_of_sale` Front End.

- Make bigger the button to reset the search input field.
