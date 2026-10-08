Customize OCA / product-attribute / `product_category_active` module.

- Remove default value for the field `categ_id` of the model
  `product.template` to force user to select a category and have the
  possibility to disable the "All" category.

Note: we don't remove `categ_id` in "install mode", or in some situation
where the ORM create automatically products (like in `loyalty` module).
In that case, we just warn the user with the `web_notify` module.
