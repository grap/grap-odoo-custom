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


**Product Changes**
Add extra constraint on product if ``income_pdt`` or ``expense_pdt``
are checked:

* This product are manage by account manager only
* this product must have account_income (or account_expense) defined
* This product must have only one VAT (if ``expense_pdt`` is checked)
* this product can not be ``sale_ok`` or ``purchase_ok``


**Groups**

Add a new Custom group category.

Add new groups :

* GRAP - Buyer / Reseller
* GRAP - Transformer
* GRAP - CRM and Calendar Manager
* GRAP - Pricelist Manager
