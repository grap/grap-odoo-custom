Customize Odoo / odoo / ``sale`` module. (and pseudo sales modules
``sales_team``, ``sale_management`` modules.)

* Display for members of ``sales_team.group_sale_salesman_all_leads``
  the following menu entries:
  * "Sale > Analysis"
  * "Sale > Configuration"

* Give access to ``sale.order.template`` model (and related
  ``sale.order.template.line`` and ``sale.order.template.option`` models)
  for members of ``sales_team.group_sale_salesman_all_leads``.

* On ``sale.order`` form:
  * move fiscal position field from Other Info tab, to main form.
