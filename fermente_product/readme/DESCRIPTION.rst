Customize Odoo / odoo / ``product`` module.

* Remove default value for the field ``categ_id`` of the model ``product.template``
  to force user to select a category and have the possibility to disable the "All"
  category.

* Set default ``list`` view for product, and not ``kanban`` (save planet and ressources).
  (A product image is one server call)