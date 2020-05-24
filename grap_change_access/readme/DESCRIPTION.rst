This module extends the functionality of Odoo to change access.

**Prevent Update/Delete Access for users**

For users that doesn't belong to ``base.group_no_one``, the following models
are readonly

* ``product.category``
* ``product.uom``
* ``product.uom.categ``
* ``res.country``
* ``res.country.state``
* ``email.template``
* ``account.period`` (except for account manager)

**Groups**

Add a new Custom group category, named 'GRAP - Custom Category'

Add new groups :

* GRAP - Buying / Reselling Category
* GRAP - Transformation Category
* GRAP - Raw Materials Category
* GRAP - CRM and Calendar Manager
* GRAP - Pricelist Manager
