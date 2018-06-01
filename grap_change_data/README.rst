.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=========================
GRAP Custom - Change Data
=========================

This module extends the functionality of product and l10n_fr to changes
default data that doesn't fit with GRAP needs.


Model changes
=============

* Add an 'active' field on ```product.category```
* Add an 'active' field on ```account.account.template```

Data changes
============

product.category
----------------

* Disable two useless data 'All' and 'All / Saleable'

account.account.template
------------------------

Change default french accounting setting

* 445711 : TVA collectée (Taux Plein) -> TVA collectée 20%
* 445712 : TVA collectée (Taux Intermédiaire) -> TVA collectée 5.5%
* 601 -> change from view to normal type
* disable some account template
* etc

Contributors
------------

* Quentin DUPONT <quentin.dupont@grap.coop>
* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Do not contact contributors directly about support or help with technical issues.

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
