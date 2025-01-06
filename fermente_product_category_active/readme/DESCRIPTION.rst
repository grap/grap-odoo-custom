Customize OCA / product-attribute / ``product_category_active`` module.

* Remove default value for the field ``categ_id`` of the model ``product.template``
  to force user to select a category and have the possibility to disable the "All"
  category.

Note: the default is False if the category is disabled. So, tests
are not failing if categ_id is not defined in demo data or in creation of products in tests mode.
