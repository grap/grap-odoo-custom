.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=====================
GRAP Custom - l10n_fr
=====================

This module extends the functionality of french Accounting module
to make easy the creation of taxes and accounts for GRAP.

``account.tax.template`` Model
------------------------------

* Add a new field ``active``

``account.tax.template`` Datas
------------------------------

* Rename ``name`` : TVA <achat/vente> <xx%> basé sur prix <HT/TTC>
* Rename ``code`` : TVA-<HA/VT>-xx.x-<HT/TTC>
* Disable VAT with 8,5% rate

``account.account.template`` Datas
----------------------------------

* Create specific accounts

``account.tax.code.template`` Datas
-----------------------------------

* Add EBP code

Credits
=======

Contributors
------------

* Quentin DUPONT <quentin.dupont@grap.coop>
* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
