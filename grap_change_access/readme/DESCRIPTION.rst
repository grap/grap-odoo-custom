This module extends the functionality of Odoo to change access.

Changes access to certains models
---------------------------------

* **Sales / User: All Documents** (``sales_team.group_sale_salesman_all_leads``)

-> full access on ``product.margin.classification``.
-> full access on ``product.product``, ``product.template`` and ``product.price.history``
-> full access on ``product.pricetag.type``
-> full access on ``sale.order.template``, ``sale.order.template.line``, ``sale.order.template.option``

* **Point of Sale / User** (``point_of_sale.group_pos_user``)

-> full access on ``pos.category``
-> full access on ``restaurant.floor``, ``restaurant.table``

* **Inventory / User** (``stock.group_stock_user``)

-> full access on ``stock.inventory.line``.

* **Purchase / User** (``purchase.group_purchase_user``)

-> full access on ``product.supplierinfo``.


New Groups
----------

Add a new Custom group category, named 'GRAP - Custom Category'

Add new groups :

* GRAP - Buying / Reselling Category
* GRAP - Transformation Category
* GRAP - Raw Materials Category

* GRAP - Pricelist Manager to manage ``product.pricelist`` and ``product.pricelist.item``
