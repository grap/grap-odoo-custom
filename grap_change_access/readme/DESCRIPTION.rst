This module extends the functionality of Odoo to change access.

**Add roles**

based on the module ``base_user_role``.

**Changes access to certains models**

Sales / User: All Documents (``sales_team.group_sale_salesman_all_leads``)
- can write ``product.margin.classification``.

Point of Sale / User (``point_of_sale.group_pos_user``)
- can write ``pos.category``.

**Groups**

Add a new Custom group category, named 'GRAP - Custom Category'

Add new groups :

* GRAP - Buying / Reselling Category
* GRAP - Transformation Category
* GRAP - Raw Materials Category

* GRAP - Pricelist Manager to manage ``product.pricelist`` and ``product.pricelist.item``
