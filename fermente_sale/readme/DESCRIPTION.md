Customize Odoo / odoo / `sale` module. (and pseudo sales modules
`sales_team`, `sale_management` modules.)

- Display for members of `sales_team.group_sale_salesman_all_leads` the
  following menu entries:
  - "Sale \> Analysis"
  - "Sale \> Configuration"
- Give access to `sale.order.template` model (and related
  `sale.order.template.line` and `sale.order.template.option` models)
  for members of `sales_team.group_sale_salesman_all_leads`.
- On `sale.order` form:
  - move fiscal position field from Other Info tab, to main form.
  - put the 3 date (Create / Delivery and Expirate dates) at the same places
    and allways visible.
- On `sale.order` report and portal view:
  - add "Delivery Date".
- set `company_id` field as required on `sale.order.template` model,
  and put a default value to the current company.
