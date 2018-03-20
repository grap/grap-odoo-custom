.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===================================
GRAP - Change access for GRAP users
===================================

Remove update / delete access for basic users for some model

Features
--------

For users that doesn't belong to ``base.group_no_one``, the following models
   are readonly

* ``product_category`` is readonly
* ``product_uom`` is readonly
* ``product_uom_categ`` is readonly
* ``res_country`` is readonly
* ``res_country_state`` is readonly
* ``email_template`` is readonly
* ``account_period`` is readonly (except for account_manager)


Add extra constraint on product if income_pdt or expense_pdt:

* This product are manage by account manager only
* this product must have account_income (or account_expense)
* This product must have only one VAT (if expense_pdt)
* this product can not be 'sale_ok' or 'purchase_ok'

Add two new groups

* GRAP - CRM and Calendar Manager
* GRAP - Pricelist Manager

Contributors
------------

* Julien WESTE
* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Do not contact contributors directly about support or help with technical issues.

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
